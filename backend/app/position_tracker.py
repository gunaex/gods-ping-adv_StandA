"""
Position Tracker
Calculates current holdings and enables incremental position building
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Trade
from typing import Dict, Optional


def calculate_position_pl(current_position: Dict, current_price: float) -> Dict:
    """
    Calculate P/L for current position.
    
    Args:
        current_position: Position dict from get_current_position()
        current_price: Current market price
        
    Returns:
        {
            "current_value": 2750.0,  # Current market value
            "cost_basis": 2500.0,  # Total cost including fees
            "pl_amount": 250.0,  # Profit/Loss in USD
            "pl_percent": 10.0  # Profit/Loss in percentage
        }
    """
    if current_position['quantity'] <= 0:
        return {
            "current_value": 0.0,
            "cost_basis": 0.0,
            "pl_amount": 0.0,
            "pl_percent": 0.0
        }
    
    current_value = current_position['quantity'] * current_price
    cost_basis = current_position['cost_basis']
    pl_amount = current_value - cost_basis
    pl_percent = (pl_amount / cost_basis * 100) if cost_basis > 0 else 0.0
    
    return {
        "current_value": round(current_value, 2),
        "cost_basis": round(cost_basis, 2),
        "pl_amount": round(pl_amount, 2),
        "pl_percent": round(pl_percent, 2)
    }


def get_current_position(user_id: int, symbol: str, db: Session) -> Dict:
    """
    Calculate current position for a symbol including fees.
    
    Returns:
        {
            "symbol": "BTC/USDT",
            "quantity": 0.05,  # Current holdings (BTC amount)
            "cost_basis": 2500.0,  # Total cost including fees (USD)
            "average_price": 50000.0,  # Average buy price per unit
            "total_fees_paid": 2.5,  # Cumulative trading fees
            "position_value_usd": 2500.0,  # Based on average cost
            "trades_count": 5  # Number of trades that built this position
        }
    """
    from app.models import BotConfig
    
    # Get all trades for this symbol (both paper and live)
    trades = db.query(Trade).filter(
        Trade.user_id == user_id,
        Trade.symbol == symbol,
        Trade.status.in_(['completed_paper', 'completed_live', 'completed'])
    ).order_by(Trade.timestamp).all()
    
    if not trades:
        # No trades yet - check if paper trading mode
        config = db.query(BotConfig).filter(BotConfig.user_id == user_id).first()
        if config and config.paper_trading:
            # Paper trading: Start with 50% position (simulated initial holdings)
            # This allows testing both BUY and SELL immediately
            budget = config.budget
            
            # We need current price to calculate quantity
            # Return a special flag so caller knows to get price
            return {
                "symbol": symbol,
                "quantity": 0.0,
                "cost_basis": 0.0,
                "average_price": 0.0,
                "total_fees_paid": 0.0,
                "position_value_usd": 0.0,
                "trades_count": 0,
                "_paper_initial": True,  # Flag for paper trading initial state
                "_budget": budget
            }
        
        return {
            "symbol": symbol,
            "quantity": 0.0,
            "cost_basis": 0.0,
            "average_price": 0.0,
            "total_fees_paid": 0.0,
            "position_value_usd": 0.0,
            "trades_count": 0
        }
    
    # Calculate position using FIFO (First In, First Out)
    quantity = 0.0
    cost_basis = 0.0
    total_fees = 0.0
    trades_count = 0
    
    BINANCE_FEE_RATE = 0.001  # 0.1% trading fee
    
    for trade in trades:
        trades_count += 1
        trade_amount = trade.amount  # Crypto quantity (e.g., 0.01 BTC)
        trade_price = trade.filled_price or trade.price
        trade_value = trade_amount * trade_price  # USD value
        
        # Calculate trading fee (fee is paid in the asset being received)
        if trade.side == 'BUY':
            # When buying: pay fee in crypto (you receive slightly less crypto)
            fee_in_crypto = trade_amount * BINANCE_FEE_RATE
            fee_in_usd = fee_in_crypto * trade_price
            
            # Add to position
            quantity += trade_amount - fee_in_crypto  # Net crypto received after fee
            cost_basis += trade_value  # Total USD spent (fee already deducted from quantity)
            total_fees += fee_in_usd
            
        elif trade.side == 'SELL':
            # When selling: pay fee in USD (you receive slightly less USD)
            fee_in_usd = trade_value * BINANCE_FEE_RATE
            
            # Remove from position
            quantity -= trade_amount
            cost_basis -= trade_value - fee_in_usd  # Net USD received after fee
            total_fees += fee_in_usd
    
    # Calculate average price (avoid division by zero)
    average_price = (cost_basis / quantity) if quantity > 0 else 0.0
    
    return {
        "symbol": symbol,
        "quantity": round(quantity, 8),
        "cost_basis": round(cost_basis, 2),
        "average_price": round(average_price, 2),
        "total_fees_paid": round(total_fees, 2),
        "position_value_usd": round(cost_basis, 2),  # Current value based on cost
        "trades_count": trades_count
    }


def calculate_incremental_amount(
    current_position: Dict,
    max_position_size: float,
    step_percent: float,
    action: str
) -> Dict:
    """
    Calculate how much to buy/sell based on incremental step settings.
    
    Args:
        current_position: From get_current_position()
        max_position_size: Maximum USD value for this position (from risk assessment)
        step_percent: % of max_position to trade this iteration (e.g., 10%)
        action: "BUY" or "SELL"
    
    Returns:
        {
            "action": "BUY",
            "step_amount_usd": 1000.0,  # USD value to trade this step
            "current_fill_percent": 25.0,  # Current position as % of max
            "after_fill_percent": 35.0,  # After this trade
            "can_execute": True,  # Whether trade is allowed
            "reason": "Adding 10% to existing 25% position"
        }
    """
    current_value = current_position['position_value_usd']
    current_fill_percent = (current_value / max_position_size * 100) if max_position_size > 0 else 0
    
    step_amount_usd = max_position_size * (step_percent / 100)
    
    if action == 'BUY':
        after_value = current_value + step_amount_usd
        after_fill_percent = (after_value / max_position_size * 100) if max_position_size > 0 else 0
        
        # Prevent buying beyond 100%
        if current_fill_percent >= 100:
            return {
                "action": "BUY",
                "step_amount_usd": 0.0,
                "current_fill_percent": round(current_fill_percent, 2),
                "after_fill_percent": round(current_fill_percent, 2),
                "can_execute": False,
                "reason": "Already at 100% of max position - cannot buy more"
            }
        
        # Cap at 100%
        if after_fill_percent > 100:
            step_amount_usd = max_position_size - current_value
            after_fill_percent = 100.0
            reason = f"Final {step_percent}% increment capped at 100% (adding ${step_amount_usd:.2f})"
        else:
            reason = f"Adding {step_percent}% step (${step_amount_usd:.2f}) to existing {current_fill_percent:.1f}% position"
        
        return {
            "action": "BUY",
            "step_amount_usd": round(step_amount_usd, 2),
            "current_fill_percent": round(current_fill_percent, 2),
            "after_fill_percent": round(after_fill_percent, 2),
            "can_execute": True,
            "reason": reason
        }
    
    elif action == 'SELL':
        # For selling, step_percent is % of CURRENT POSITION (not max_position)
        step_amount_usd = current_value * (step_percent / 100)
        after_value = current_value - step_amount_usd
        after_fill_percent = (after_value / max_position_size * 100) if max_position_size > 0 else 0
        
        # Prevent selling if no position
        if current_fill_percent <= 0:
            return {
                "action": "SELL",
                "step_amount_usd": 0.0,
                "current_fill_percent": 0.0,
                "after_fill_percent": 0.0,
                "can_execute": False,
                "reason": "No position to sell"
            }
        
        # Cap at 0%
        if after_fill_percent < 0:
            step_amount_usd = current_value
            after_fill_percent = 0.0
            reason = f"Final {step_percent}% exit - closing entire position (${step_amount_usd:.2f})"
        else:
            reason = f"Selling {step_percent}% step (${step_amount_usd:.2f}) from {current_fill_percent:.1f}% position"
        
        return {
            "action": "SELL",
            "step_amount_usd": round(step_amount_usd, 2),
            "current_fill_percent": round(current_fill_percent, 2),
            "after_fill_percent": round(after_fill_percent, 2),
            "can_execute": True,
            "reason": reason
        }
    
    else:
        return {
            "action": "HOLD",
            "step_amount_usd": 0.0,
            "current_fill_percent": round(current_fill_percent, 2),
            "after_fill_percent": round(current_fill_percent, 2),
            "can_execute": False,
            "reason": "HOLD signal - no trade"
        }
