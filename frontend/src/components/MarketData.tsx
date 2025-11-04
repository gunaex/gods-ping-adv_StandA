import { useEffect, useState, useRef } from 'react';
import { BarChart3 } from 'lucide-react';
import { createChart, ColorType } from 'lightweight-charts';
import { marketAPI } from '../api';

interface MarketDataProps {
  symbol: string;
  fiatCurrency: string;
}

export default function MarketData({ symbol, fiatCurrency }: MarketDataProps) {
  const [ticker, setTicker] = useState<any>(null);
  const [candles, setCandles] = useState<any[]>([]);
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<any>(null);

  useEffect(() => {
    loadMarketData();
    const interval = setInterval(loadMarketData, 10000); // Update every 10s
    return () => clearInterval(interval);
  }, [symbol]);

  useEffect(() => {
    if (candles.length > 0 && chartContainerRef.current) {
      renderChart();
    }
  }, [candles]);

  const loadMarketData = async () => {
    try {
      const [tickerRes, candlesRes] = await Promise.all([
        marketAPI.getTicker(symbol),
        marketAPI.getCandles(symbol, '1h', 100),
      ]);
      setTicker(tickerRes.data);
      setCandles(candlesRes.data.candles);
    } catch (error) {
      console.error('Failed to load market data:', error);
    }
  };

  const renderChart = () => {
    if (!chartContainerRef.current) return;

    // Clear existing chart
    if (chartRef.current) {
      chartRef.current.remove();
    }

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: 'transparent' },
        textColor: '#ffffff',
      },
      width: chartContainerRef.current.clientWidth,
      height: 400,
      grid: {
        vertLines: { color: 'rgba(255, 255, 255, 0.1)' },
        horzLines: { color: 'rgba(255, 255, 255, 0.1)' },
      },
    });

    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#4ade80',
      downColor: '#f87171',
      borderVisible: false,
      wickUpColor: '#4ade80',
      wickDownColor: '#f87171',
    });

    const formattedCandles = candles.map(c => ({
      time: c.timestamp / 1000,
      open: c.open,
      high: c.high,
      low: c.low,
      close: c.close,
    }));

    candlestickSeries.setData(formattedCandles);
    chart.timeScale().fitContent();

    chartRef.current = chart;

    // Handle resize
    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({
          width: chartContainerRef.current.clientWidth,
        });
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  };

  return (
    <div className="section-card">
      <div className="section-title">
        <BarChart3 />
        Market Data & Candlestick Chart
      </div>

      {ticker && (
        <div className="grid grid-3" style={{ marginBottom: '20px' }}>
          <div style={{
            padding: '15px',
            background: 'rgba(0, 0, 0, 0.2)',
            borderRadius: '8px',
          }}>
            <div style={{ fontSize: '0.9rem', opacity: 0.8 }}>Last Price</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
              ${ticker.last?.toFixed(2)}
            </div>
          </div>

          <div style={{
            padding: '15px',
            background: 'rgba(0, 0, 0, 0.2)',
            borderRadius: '8px',
          }}>
            <div style={{ fontSize: '0.9rem', opacity: 0.8 }}>24h Change</div>
            <div style={{
              fontSize: '1.5rem',
              fontWeight: 'bold',
              color: ticker.change_24h >= 0 ? '#4ade80' : '#f87171',
            }}>
              {ticker.change_24h >= 0 ? '+' : ''}{ticker.change_24h?.toFixed(2)}%
            </div>
          </div>

          <div style={{
            padding: '15px',
            background: 'rgba(0, 0, 0, 0.2)',
            borderRadius: '8px',
          }}>
            <div style={{ fontSize: '0.9rem', opacity: 0.8 }}>24h Volume</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
              {ticker.volume?.toFixed(0)}
            </div>
          </div>
        </div>
      )}

      <div ref={chartContainerRef} className="chart-container" />
    </div>
  );
}
