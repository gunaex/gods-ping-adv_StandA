"""
Gods Ping - FastAPI Backend
Main API endpoints for Shichi-Fukujin single-page trading platform
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.db import engine, get_db, Base
from app.models import User, Trade, BotConfig
from app.auth import (
    verify_password, get_password_hash, create_access_token, create_refresh_token,
    get_current_active_user, ensure_admin_exists, ADMIN_USERNAME,
    encrypt_api_key, decrypt_api_key
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gods Ping API",
    description="Shichi-Fukujin Trading Platform",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Models
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class CreateUserRequest(BaseModel):
    username: str
    password: str


class UpdateBotConfigRequest(BaseModel):
    symbol: Optional[str] = None
    fiat_currency: Optional[str] = None
    budget: Optional[float] = None
    paper_trading: Optional[bool] = None
    risk_level: Optional[str] = None
    min_confidence: Optional[float] = None
    position_size_ratio: Optional[float] = None
    max_daily_loss: Optional[float] = None
    grid_enabled: Optional[bool] = None
    grid_lower_price: Optional[float] = None
    grid_upper_price: Optional[float] = None
    grid_levels: Optional[int] = None
    dca_enabled: Optional[bool] = None
    dca_amount_per_period: Optional[float] = None
    dca_interval_days: Optional[int] = None
    gods_hand_enabled: Optional[bool] = None


class UpdateAPIKeysRequest(BaseModel):
    binance_api_key: str
    binance_api_secret: str


class TradeRequest(BaseModel):
    symbol: str
    side: str  # BUY or SELL
    amount: float
    price: Optional[float] = None


# Startup Event
@app.on_event("startup")
async def startup_event():
    """Initialize database with admin user"""
    db = next(get_db())
    created = ensure_admin_exists(db)
    if created:
        print(f"✅ Admin user created: {ADMIN_USERNAME}")
    else:
        print(f"✅ Admin user exists: {ADMIN_USERNAME}")
    db.close()


# Health Check
@app.get("/")
async def root():
    return {
        "app": "Gods Ping (Shichi-Fukujin)",
        "status": "running",
        "version": "1.0.0"
    }


# Authentication Endpoints
@app.post("/api/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login with username and password"""
    user = db.query(User).filter(User.username == request.username).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create tokens
    access_token = create_access_token({"user_id": user.id, "username": user.username})
    refresh_token = create_refresh_token({"user_id": user.id})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }


@app.post("/api/auth/create-user")
async def create_user(
    request: CreateUserRequest,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Admin creates one additional user"""
    # Only admin can create users
    if not current_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Only admin can create users")
    
    # Check if user already exists
    existing = db.query(User).filter(User.username == request.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check user count (max 2: admin + 1 user)
    user_count = db.query(User).count()
    if user_count >= 2:
        raise HTTPException(status_code=400, detail="Maximum user limit reached (1 additional user)")
    
    # Create new user
    new_user = User(
        username=request.username,
        hashed_password=get_password_hash(request.password),
        is_admin=False,
        is_active=True,
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create default bot config for user
    bot_config = BotConfig(user_id=new_user.id)
    db.add(bot_config)
    db.commit()
    
    return {"message": "User created successfully", "user": new_user.to_dict()}


@app.get("/api/auth/me")
async def get_me(current_user: dict = Depends(get_current_active_user)):
    """Get current user info"""
    return current_user


# User Settings & API Keys
@app.post("/api/settings/api-keys")
async def update_api_keys(
    request: UpdateAPIKeysRequest,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update Binance API keys"""
    user = db.query(User).filter(User.id == current_user["id"]).first()
    
    # Encrypt and store
    user.binance_api_key = encrypt_api_key(request.binance_api_key)
    user.binance_api_secret = encrypt_api_key(request.binance_api_secret)
    
    db.commit()
    
    return {"message": "API keys updated successfully"}


@app.get("/api/settings/bot-config")
async def get_bot_config(
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's bot configuration"""
    config = db.query(BotConfig).filter(BotConfig.user_id == current_user["id"]).first()
    
    if not config:
        # Create default config
        config = BotConfig(user_id=current_user["id"])
        db.add(config)
        db.commit()
        db.refresh(config)
    
    return config.to_dict()


@app.put("/api/settings/bot-config")
async def update_bot_config(
    request: UpdateBotConfigRequest,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update bot configuration (unified settings)"""
    config = db.query(BotConfig).filter(BotConfig.user_id == current_user["id"]).first()
    
    if not config:
        config = BotConfig(user_id=current_user["id"])
        db.add(config)
    
    # Update fields
    update_data = request.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(config, field, value)
    
    config.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(config)
    
    return config.to_dict()


# Trading Pairs
@app.get("/api/trading-pairs")
async def get_trading_pairs():
    """Get supported trading pairs"""
    return {
        "pairs": [
            {"symbol": "ETH/USDT", "name": "Ethereum"},
            {"symbol": "BTC/USDT", "name": "Bitcoin"},
            {"symbol": "BNB/USDT", "name": "Binance Coin"},
            {"symbol": "SOL/USDT", "name": "Solana"},
            {"symbol": "XRP/USDT", "name": "Ripple"},
            {"symbol": "USDC/USDT", "name": "USD Coin"},
            {"symbol": "ADA/USDT", "name": "Cardano"},
            {"symbol": "DOGE/USDT", "name": "Dogecoin"},
            {"symbol": "DOT/USDT", "name": "Polkadot"},
        ],
        "fiat_currencies": ["USD", "THB"]
    }


# Market Data (delegated to market.py)
@app.get("/api/market/ticker/{symbol}")
async def get_ticker(symbol: str):
    """Get current ticker price"""
    from app.market import get_current_price, convert_to_fiat
    
    try:
        price_data = await get_current_price(symbol)
        return price_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market/candles/{symbol}")
async def get_candles(symbol: str, timeframe: str = "1h", limit: int = 100):
    """Get candlestick data"""
    from app.market import get_candlestick_data
    
    try:
        candles = await get_candlestick_data(symbol, timeframe, limit)
        return {"symbol": symbol, "timeframe": timeframe, "candles": candles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market/orderbook/{symbol}")
async def get_orderbook(symbol: str, limit: int = 20):
    """Get orderbook depth"""
    from app.market import get_order_book
    
    try:
        orderbook = await get_order_book(symbol, limit)
        return orderbook
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# AI Recommendations
@app.get("/api/ai/recommendation/{symbol}")
async def get_ai_recommendation(
    symbol: str,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get AI trading recommendation"""
    from app.ai_engine import get_trading_recommendation
    
    try:
        config = db.query(BotConfig).filter(BotConfig.user_id == current_user["id"]).first()
        recommendation = await get_trading_recommendation(symbol, config)
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ai/analysis/{symbol}")
async def get_advanced_analysis(
    symbol: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Get advanced AI market analysis"""
    from app.ai_engine import get_advanced_analysis
    
    try:
        analysis = await get_advanced_analysis(symbol)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Trading
@app.post("/api/trade/execute")
async def execute_trade(
    request: TradeRequest,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Execute a trade (manual or bot)"""
    config = db.query(BotConfig).filter(BotConfig.user_id == current_user["id"]).first()
    
    # Create trade record
    trade = Trade(
        user_id=current_user["id"],
        symbol=request.symbol,
        side=request.side,
        amount=request.amount,
        price=request.price,
        bot_type="manual",
        status="pending",
        timestamp=datetime.utcnow()
    )
    db.add(trade)
    db.commit()
    db.refresh(trade)
    
    if config and config.paper_trading:
        # Paper trading
        trade.status = "completed_paper"
        trade.filled_price = request.price
        db.commit()
        return {"message": "Paper trade executed", "trade_id": trade.id, "status": "paper"}
    else:
        # Real trading (implement with ccxt)
        from app.market import execute_market_trade
        try:
            result = await execute_market_trade(
                current_user["id"], 
                request.symbol, 
                request.side, 
                request.amount,
                db
            )
            trade.status = "completed"
            trade.filled_price = result.get("price")
            db.commit()
            return {"message": "Trade executed", "trade_id": trade.id, "result": result}
        except Exception as e:
            trade.status = "failed"
            db.commit()
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/trade/history")
async def get_trade_history(
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get user's trade history"""
    trades = db.query(Trade).filter(
        Trade.user_id == current_user["id"]
    ).order_by(Trade.timestamp.desc()).limit(limit).all()
    
    return [
        {
            "id": t.id,
            "symbol": t.symbol,
            "side": t.side,
            "amount": t.amount,
            "price": t.price,
            "filled_price": t.filled_price,
            "status": t.status,
            "bot_type": t.bot_type,
            "timestamp": t.timestamp.isoformat()
        }
        for t in trades
    ]


# Bot Controls
@app.post("/api/bot/grid/start")
async def start_grid_bot(
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Start Grid Bot"""
    from app.bots import start_grid_bot as run_grid
    
    config = db.query(BotConfig).filter(BotConfig.user_id == current_user["id"]).first()
    if not config or not config.grid_enabled:
        raise HTTPException(status_code=400, detail="Grid bot not configured")
    
    result = await run_grid(current_user["id"], config, db)
    return result


@app.post("/api/bot/dca/start")
async def start_dca_bot(
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Start DCA Bot"""
    from app.bots import start_dca_bot as run_dca
    
    config = db.query(BotConfig).filter(BotConfig.user_id == current_user["id"]).first()
    if not config or not config.dca_enabled:
        raise HTTPException(status_code=400, detail="DCA bot not configured")
    
    result = await run_dca(current_user["id"], config, db)
    return result


@app.post("/api/bot/gods-hand/start")
async def start_gods_hand(
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Start Gods Hand autonomous trading"""
    from app.bots import start_gods_hand as run_gods_hand
    
    config = db.query(BotConfig).filter(BotConfig.user_id == current_user["id"]).first()
    if not config or not config.gods_hand_enabled:
        raise HTTPException(status_code=400, detail="Gods Hand not enabled")
    
    result = await run_gods_hand(current_user["id"], config, db)
    return result


@app.post("/api/bot/{bot_type}/stop")
async def stop_bot(
    bot_type: str,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Stop a running bot"""
    from app.bots import stop_bot as stop_running_bot
    
    result = await stop_running_bot(bot_type, current_user["id"], db)
    return result


@app.get("/api/bot/status")
async def get_bot_status(
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get status of all bots"""
    from app.bots import get_bot_status as check_status
    
    status = await check_status(current_user["id"], db)
    return status


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
