/**
 * Market Ticker - FinSense (Localized Dashboard Version)
 * Fetches real-time stock and crypto data to display in the dashboard area.
 */

async function initMarketTicker() {
    const container = document.getElementById('market-ticker-container');
    if (!container) return; // Only run on pages with the container

    const bar = document.createElement('div');
    bar.className = 'market-ticker-bar';
    bar.innerHTML = '<div class="ticker-scroll-wrapper" id="market-ticker-content"></div>';
    container.appendChild(bar);

    const tickerContent = document.getElementById('market-ticker-content');

    async function updateData() {
        try {
            const response = await fetch('/api/market-ticker');
            if (!response.ok) throw new Error('Failed to fetch ticker data');
            
            const data = await response.json();
            if (!data || data.length === 0) return;

            tickerContent.innerHTML = '';
            
            const createItem = (item) => {
                const div = document.createElement('div');
                div.className = `market-item ${item.positive ? 'positive' : 'negative'}`;
                // Using dynamic currency symbol (R$ or $)
                div.innerHTML = `
                    <span class="symbol">${item.symbol}</span>
                    <span class="price">${item.currency} ${item.price}</span>
                    <span class="variation">(${item.change})</span>
                `;
                return div;
            };

            // Double duplicate for smooth infinite scroll
            const items = [...data, ...data, ...data];
            items.forEach(item => {
                tickerContent.appendChild(createItem(item));
            });

        } catch (error) {
            console.error('Ticker Error:', error);
            tickerContent.innerHTML = '<div class="market-item">⚠️ Erro ao carregar cotações</div>';
        }
    }

    await updateData();
    setInterval(updateData, 300000);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMarketTicker);
} else {
    initMarketTicker();
}
