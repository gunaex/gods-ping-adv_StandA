"""
Trading Bots Service
Grid Bot, DCA Bot, and Gods Hand Autonomous Trading
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional
from sqlalchemy.orm import Session
from app.models import BotConfig, Trade
from app.market import get_current_price, execute_market_trade
from app.ai_engine import get_trading_recommendation, calculate_risk_assessment


# Bot status tracking (in-memory, use Redis in production)
bot_status = {}
bot_tasks = {}


async def start_grid_bot(user_id: int, config: BotConfig, db: Session) -> dict:
    """
    Start Grid Trading Bot
    Places buy/sell orders at predefined price levels
    """
    if f"grid_{user_id}" in bot_status:
        return {"status": "error", "message": "Grid bot already running"}
    
    bot_status[f"grid_{user_id}"] = "running"
    
    try:
        symbol = config.symbol
        lower_price = config.grid_lower_price
        upper_price = config.grid_upper_price
        levels = config.grid_levels
        budget = config.budget
        
        # Calculate grid levels
        price_step = (upper_price - lower_price) / levels
        grid_levels_prices = [lower_price + i * price_step for i in range(levels + 1)]
        
        # Calculate amount per level
        amount_per_level = budget / levels
        
        # Get current price
        ticker = await get_current_price(symbol)
        current_price = ticker['last']
        
        # Paper trading simulation
        if config.paper_trading:
            trades_placed = []
            
            # Place buy orders below current price
            for price in grid_levels_prices:
                if price < current_price:
                    trade = Trade(
                        user_id=user_id,
                        symbol=symbol,
                        side="BUY",
                        amount=amount_per_level / price,
                        price=price,
                        filled_price=price,
                        status="completed_paper",
                        bot_type="grid",
                        timestamp=datetime.utcnow()
                    )
                    db.add(trade)
                    trades_placed.append({"side": "BUY", "price": price})
                
                # Place sell orders above current price
                elif price > current_price:
                    trade = Trade(
                        user_id=user_id,
                        symbol=symbol,
                        side="SELL",
                        amount=amount_per_level / price,
                        price=price,
                        filled_price=price,
                        status="completed_paper",
                        bot_type="grid",
                        timestamp=datetime.utcnow()
                    )
                    db.add(trade)
                    trades_placed.append({"side": "SELL", "price": price})
            
            db.commit()
            
            return {
                "status": "success",
                "mode": "paper",
                "symbol": symbol,
                "grid_levels": grid_levels_prices,
                "trades_placed": len(trades_placed),
                "message": f"Grid bot started (paper trading) with {levels} levels"
            }
        
        else:
            # Real trading (simplified - full implementation requires order monitoring)
            return {
                "status": "success",
                "mode": "live",
                "symbol": symbol,
                "message": "Grid bot started (live trading)",
                "note": "Full implementation requires continuous order monitoring"
            }
            
    except Exception as e:
        bot_status[f"grid_{user_id}"] = "error"
        return {"status": "error", "message": str(e)}


async def start_dca_bot(user_id: int, config: BotConfig, db: Session) -> dict:
    """
    Start DCA (Dollar Cost Averaging) Bot
    Buys at regular intervals regardless of price
    """
    if f"dca_{user_id}" in bot_status:
        return {"status": "error", "message": "DCA bot already running"}
    
    bot_status[f"dca_{user_id}"] = "running"
    
    try:
        symbol = config.symbol
        amount_per_period = config.dca_amount_per_period
        interval_days = config.dca_interval_days
        
        # Get current price
        ticker = await get_current_price(symbol)
        current_price = ticker['last']
        
        # Calculate buy amount
        buy_amount = amount_per_period / current_price
        
        if config.paper_trading:
            # Execute paper trade
            trade = Trade(
                user_id=user_id,
                symbol=symbol,
                side="BUY",
                amount=buy_amount,
                price=current_price,
                filled_price=current_price,
                status="completed_paper",
                bot_type="dca",
                timestamp=datetime.utcnow()
            )
            db.add(trade)
            db.commit()
            
            next_buy = datetime.utcnow() + timedelta(days=interval_days)
            
            return {
                "status": "success",
                "mode": "paper",
                "symbol": symbol,
                "amount": buy_amount,
                "price": current_price,
                "next_buy": next_buy.isoformat(),
                "message": f"DCA buy executed (paper). Next buy in {interval_days} days"
            }
        else:
            # Real trading
            result = await execute_market_trade(user_id, symbol, "BUY", buy_amount, db)
            
            return {
                "status": "success",
                "mode": "live",
                "result": result,
                "message": "DCA buy executed (live)"
            }
            
    except Exception as e:
        bot_status[f"dca_{user_id}"] = "error"
        return {"status": "error", "message": str(e)}


async def start_gods_hand(user_id: int, config: BotConfig, db: Session) -> dict:
    """
    Start Gods Hand - Autonomous AI Trading System
    Uses AI recommendations with risk management
    """
    if f"gods_hand_{user_id}" in bot_status:
        return {"status": "error", "message": "Gods Hand already running"}
    
    bot_status[f"gods_hand_{user_id}"] = "running"
    
    try:
        symbol = config.symbol
        
        # Get AI recommendation
        recommendation = await get_trading_recommendation(symbol, config)
        
        # Get risk assessment
        risk_assessment = await calculate_risk_assessment(symbol, config)
        
        action = recommendation['action']
        confidence = recommendation['confidence']
        
        # Check if confidence meets minimum threshold
        if confidence < config.min_confidence:
            return {
                "status": "hold",
                "mode": "paper" if config.paper_trading else "live",
                "symbol": symbol,
                "reason": f"Confidence {confidence} below minimum {config.min_confidence}",
                "recommendation": recommendation,
                "risk_assessment": risk_assessment
            }
        
        # Execute trade based on AI recommendation
        if action in ['BUY', 'SELL']:
            amount = risk_assessment['recommended_position_size']
            current_price = risk_assessment['current_price']
            
            if config.paper_trading:
                # Paper trade
                trade = Trade(
                    user_id=user_id,
                    symbol=symbol,
                    side=action,
                    amount=amount / current_price if action == 'BUY' else amount,
                    price=current_price,
                    filled_price=current_price,
                    status="completed_paper",
                    bot_type="gods_hand",
                    timestamp=datetime.utcnow()
                )
                db.add(trade)
                db.commit()
                
                return {
                    "status": "success",
                    "mode": "paper",
                    "action": action,
                    "symbol": symbol,
                    "amount": amount,
                    "price": current_price,
                    "confidence": confidence,
                    "recommendation": recommendation,
                    "risk_assessment": risk_assessment,
                    "message": f"Gods Hand executed {action} (paper trading)"
                }
            else:
                # Real trading
                trade_amount = amount / current_price if action == 'BUY' else amount
                result = await execute_market_trade(user_id, symbol, action, trade_amount, db)
                
                return {
                    "status": "success",
                    "mode": "live",
                    "action": action,
                    "result": result,
                    "confidence": confidence,
                    "recommendation": recommendation,
                    "risk_assessment": risk_assessment,
                    "message": f"Gods Hand executed {action} (live trading)"
                }
        else:
            # HOLD
            return {
                "status": "hold",
                "mode": "paper" if config.paper_trading else "live",
                "symbol": symbol,
                "recommendation": recommendation,
                "risk_assessment": risk_assessment,
                "message": "Gods Hand recommends HOLD"
            }
            
    except Exception as e:
        bot_status[f"gods_hand_{user_id}"] = "error"
        return {"status": "error", "message": str(e)}


async def stop_bot(bot_type: str, user_id: int, db: Session) -> dict:
    """Stop a running bot"""
    bot_key = f"{bot_type}_{user_id}"
    
    if bot_key in bot_status:
        bot_status[bot_key] = "stopped"
        
        # Cancel any background tasks
        if bot_key in bot_tasks:
            bot_tasks[bot_key].cancel()
            del bot_tasks[bot_key]
        
        return {
            "status": "success",
            "message": f"{bot_type} bot stopped"
        }
    else:
        return {
            "status": "info",
            "message": f"{bot_type} bot is not running"
        }


async def get_bot_status(user_id: int, db: Session) -> dict:
    """Get status of all bots for user"""
    return {
        "grid": bot_status.get(f"grid_{user_id}", "stopped"),
        "dca": bot_status.get(f"dca_{user_id}", "stopped"),
        "gods_hand": bot_status.get(f"gods_hand_{user_id}", "stopped"),
        "timestamp": datetime.utcnow().isoformat()
    }
