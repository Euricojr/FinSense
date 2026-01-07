
        function toggleMenu() {
            const nav = document.getElementById('main-nav');
            nav.classList.toggle('active');
        }
        
        function closeMenu() {
            const nav = document.getElementById('main-nav');
            if(window.innerWidth <= 768) {
                nav.classList.remove('active');
            }
        }

        // --- API Base URL Logic ---
        // --- API Base URL Logic ---
        function getBaseUrl() {
            const hostname = window.location.hostname;
            const port = window.location.port;

            // Auto-Redirect Live Server (5500) to Flask (5000)
            if (port === '5500' && (hostname === '127.0.0.1' || hostname === 'localhost')) {
                // Determine target path
                let path = window.location.pathname;
                
                // Fix path: remove /templates/ if present logic is tricky, 
                // typically Live Server serves /templates/index2.html
                // Flask serves / (for index2.html) or /login
                
                if (path.includes('index2.html')) {
                    window.location.href = 'http://127.0.0.1:5000/';
                    return 'http://127.0.0.1:5000'; // Unreachable but safe
                }
                
                // For other files, try to map to route
                // e.g. /templates/login.html -> /login
                // But wait, the files are just 'login' in the href now.
                // If user is on 5500 and clicks 'login', it goes to /templates/login (404)
                // This script runs on the PAGE load. If 404, script doesn't run.
                
                // So this redirect helps if they land on a valid HTML page like index2.html
                // But it won't fix the 404 page itself unless we inject script there (we can't).
                
                // However, if we redirect index2.html immediately, they get to the right place.
                window.location.href = 'http://127.0.0.1:5000' + path.replace('/templates', '').replace('.html', '');
                return 'http://127.0.0.1:5000';
            }

            if ((hostname === '127.0.0.1' || hostname === 'localhost') && port !== '5000') {
                 return 'http://127.0.0.1:5000';
            }
            return '';
        }
        const API_BASE_URL = getBaseUrl();

        // Modal Functions
        function showModal() {
            const modal = document.getElementById('login-modal');
            if (modal) modal.style.display = 'flex';
        }

        function closeModal() {
            const modal = document.getElementById('login-modal');
            if (modal) modal.style.display = 'none';
        }

        // --- AUTH LOGIC ---
        let isUserAuthenticated = false;

        async function checkAuth() {
            try {
                const response = await fetch(`${API_BASE_URL}/api/me`);
                if (response.ok) {
                    const data = await response.json();
                    const navPublic = document.getElementById('nav-public');
                    const navAuth = document.getElementById('nav-auth');
                    const usernameDisplay = document.getElementById('username-display');

                    if (data.authenticated) {
                        isUserAuthenticated = true;
                        if(navPublic) navPublic.style.display = 'none';
                        if(navAuth) navAuth.style.display = 'flex';
                        if(usernameDisplay) usernameDisplay.textContent = data.username;
                        return;
                    }
                }
            } catch (e) {
                console.log("Auth check failed:", e);
            }
            // Default: Show Public
            isUserAuthenticated = false;
            const navPublic = document.getElementById('nav-public');
            const navAuth = document.getElementById('nav-auth');
            if(navPublic) navPublic.style.display = 'flex';
            if(navAuth) navAuth.style.display = 'none';
        }

        async function logout() {
            try {
                await fetch(`${API_BASE_URL}/logout`);
                window.location.href = '/';
            } catch (e) {
                console.error("Logout failed", e);
                window.location.href = '/';
            }
        }

        // Intercept Protected Links with Modal
        document.addEventListener('DOMContentLoaded', () => {
            const protectedLinks = document.querySelectorAll('.protected-link');
            protectedLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    if (!isUserAuthenticated) {
                        e.preventDefault();
                        showModal();
                    }
                });
            });

            // Close modal on outside click
            document.getElementById('login-modal')?.addEventListener('click', (e) => {
                if (e.target === e.currentTarget) closeModal();
            });
        });



        // Init
        checkAuth();

        // --- API Config (Auth Logic handled above) ---
        // ------------------

        // --- Configuração Plotly (Dynamic Theme) ---
        const plotConfig = { responsive: true, displayModeBar: false, locale: 'pt-BR' };

        function getPlotLayout() {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const bgColor = isDark ? '#112240' : '#ffffff';
            const gridColor = isDark ? '#233554' : '#e0e0e0';
            const textColor = isDark ? '#e6f1ff' : '#1a1a1a';

            return {
                paper_bgcolor: bgColor,
                plot_bgcolor: bgColor,
                font: { color: textColor, family: 'Manrope, sans-serif' },
                margin: { t: 30, l: 60, r: 40, b: 60 },
                xaxis: {
                    gridcolor: gridColor,
                    // tickangle: -30, // Let Plotly handle angle
                    automargin: true
                },
                yaxis: {
                    gridcolor: gridColor,
                    autorange: true,
                    fixedrange: false
                }
            };
        }


        // --- Theme Logic ---
        function toggleTheme() {
            const html = document.documentElement;
            const current = html.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';

            html.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);

            // Update button icon
            const btn = document.getElementById('theme-btn');
            btn.innerText = next === 'dark' ? '☀️' : '🌙';

            // Refresh chart to apply new theme
            mudouAtivo();
            carregarHeatmap();
        }

        function loadTheme() {
            const saved = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-theme', saved);
            const btn = document.getElementById('theme-btn');
            if (btn) btn.innerText = saved === 'dark' ? '☀️' : '🌙';
        }

        function toggleSpinner(id, show) {
            const el = document.getElementById(id);
            if (el) {
                if (show) el.classList.add('active');
                else el.classList.remove('active');
            }
        }

        // --- Multiselect Logic ---
        function toggleMultiselect() {
            const menu = document.getElementById('multiselect-menu');
            menu.classList.toggle('active');
        }

        // Helper to toggle checkbox when clicking the row
        function toggleCheck(id) {
            // Prevent double toggle if clicking the checkbox itself
            if (event.target.type === 'checkbox') return;

            const check = document.getElementById(id);
            check.checked = !check.checked;
            mudouAtivo();
        }

        // Close dropdown when clicking outside
        document.addEventListener('click', function (event) {
            const container = document.querySelector('.multiselect-container');
            const menu = document.getElementById('multiselect-menu');
            if (container && !container.contains(event.target)) {
                menu.classList.remove('active');
            }
        });

        // --- Search & Autocomplete Logic ---
        let allAssets = [];

        async function fetchAssets() {
            try {
                const response = await fetch(`${API_BASE_URL}/api/assets`);
                if (response.ok) {
                    allAssets = await response.json();
                    filterSidebar(); // Initial render with default filter
                }
            } catch (e) {
                console.error("Error loading assets:", e);
            }
        }

        async function filterSidebar() {
            const categoryObj = document.getElementById('sidebar-category');
            if(!categoryObj) return;

            const category = categoryObj.value;
            const list = document.getElementById('lista-ativos-lateral'); // To show loading

            if (category === 'all') {
                // 'All' is too heavy to fetch live prices for everything at once in this architecture
                // Show static list (prices will be '---')
                renderSidebarList(allAssets);
                return;
            }

            // Show loading in sidebar
            if (list) {
                const loadingText = (window.translations && window.translations[currentLang] && window.translations[currentLang].sidebar_loading) 
                                   ? window.translations[currentLang].sidebar_loading 
                                   : 'Carregando preços...';
                list.innerHTML = `<li style="padding:20px; text-align:center; color:var(--text-muted);">${loadingText}</li>`;
            }

            try {
                // Use heatmap endpoint which returns [{symbol, name, price, change, ...}]
                const response = await fetch(`${API_BASE_URL}/api/heatmap?type=${category}`);
                if (response.ok) {
                    const data = await response.json();
                    renderSidebarList(data);
                } else {
                    // Fallback to static if error
                    console.error("Error fetching live sidebar data");
                    // Filter static list as fallback
                    const filtered = allAssets.filter(asset => (asset.category || '') === category);
                    renderSidebarList(filtered); 
                }
            } catch (e) {
                console.error("Fetch error:", e);
                // Fallback
                const filtered = allAssets.filter(asset => (asset.category || '') === category);
                renderSidebarList(filtered);
            }
        }
        
        function renderSidebarList(assets) {
            const list = document.getElementById('lista-ativos-lateral');
            if (!list) return;
            list.innerHTML = '';
            
            assets.forEach(asset => {
                const li = document.createElement('li');
                li.className = 'asset-item';
                li.onclick = () => selecionarAtivo(asset.symbol, li);
                if (asset.symbol === document.getElementById('ativo-atual').value) {
                    li.classList.add('active');
                }
                
                // Hax: price might be missing from /api/assets
                const price = asset.price !== undefined ? asset.price : 0;
                const change = asset.change !== undefined ? asset.change : 0;
                
                const isPositive = change >= 0;
                const changeClass = isPositive ? 'positive' : 'negative';
                const sign = isPositive ? '+' : '';
                
                const priceStr = asset.price !== undefined ? `$${price.toFixed(2)}` : '---';
                const changeStr = asset.change !== undefined ? `${sign}${change.toFixed(2)}%` : '---';
                
                li.innerHTML = `
                    <div class="asset-info">
                        <span class="asset-symbol">${asset.symbol}</span>
                        <span class="asset-name">${asset.name || asset.symbol}</span>
                    </div>
                    <div class="asset-price-info">
                        <div class="asset-price">${priceStr}</div>
                        <div class="asset-change ${changeClass}">${changeStr}</div>
                    </div>
                `;
                list.appendChild(li);
            });
        }

        function setupAutocomplete() {
            const input = document.getElementById('asset-search');
            const suggestions = document.getElementById('suggestions');

            input.addEventListener('input', (e) => {
                const query = e.target.value.toLowerCase().trim();

                if (query.length < 1) {
                    suggestions.style.display = 'none';
                    return;
                }

                const matches = allAssets.filter(asset =>
                    (asset.symbol && asset.symbol.toLowerCase().includes(query)) ||
                    (asset.name && asset.name.toLowerCase().includes(query))
                ).slice(0, 10);

                renderSuggestions(matches);
            });

            // Hide on click outside
            document.addEventListener('click', (e) => {
                if (!input.contains(e.target) && !suggestions.contains(e.target)) {
                    suggestions.style.display = 'none';
                }
            });
        }

        function renderSuggestions(matches) {
            const suggestions = document.getElementById('suggestions');
            suggestions.innerHTML = '';

            if (matches.length === 0) {
                suggestions.style.display = 'none';
                return;
            }

            matches.forEach(asset => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span><strong>${asset.symbol}</strong> - ${asset.name}</span>
                    <span style="font-size: 11px; opacity: 0.7; text-transform: uppercase;">${asset.category}</span>
                `;

                li.onclick = () => {
                    selecionarAtivo(asset.symbol, null);
                    suggestions.style.display = 'none';
                    document.getElementById('asset-search').value = '';
                };

                suggestions.appendChild(li);
            });

            suggestions.style.display = 'block';
        }

        function selecionarAtivo(ticker, elementoDOM) {
            document.getElementById('ativo-atual').value = ticker;

            document.querySelectorAll('.asset-item').forEach(el => el.classList.remove('active'));
            if (elementoDOM) elementoDOM.classList.add('active');

            mudouAtivo();
        }

        // --- Heatmap (Plotly Treemap) Logic ---
        async function carregarHeatmap() {
            const loader = document.getElementById('heatmap-loader');

            // Show loader
            if (loader) loader.classList.add('active');

            try {
                const categoria = document.getElementById('heatmap-category').value;
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 60000); // 60s timeout for Render Free Tier

                const response = await fetch(`${API_BASE_URL}/api/heatmap?type=${categoria}`, { signal: controller.signal });
                clearTimeout(timeoutId);

                const dados = await response.json();

                if (!dados || dados.length === 0) {
                    document.getElementById('heatmap-plot').innerHTML = '<div style="text-align: center; padding: 50px; color: var(--text-muted);">Sem dados disponíveis</div>';
                    return;
                }

                // Prepare data for Treemap
                const labels = [];
                const parents = [];
                const values = []; // Size (abs change)
                const texts = [];  // Display text
                const colors = []; // Colors based on change

                const categoryNames = {
                    'cripto': 'Criptomoedas',
                    'br': 'Ações Brasil',
                    'us': 'Ações EUA',
                    'indices': 'Índices Globais'
                };
                const rootLabel = categoryNames[categoria] || "Mercado";

                dados.forEach(ativo => {
                    labels.push(ativo.symbol);
                    parents.push(rootLabel); // Group all under the category

                    // Size: Absolute value of change (min size 0.1 to show even small changes)
                    values.push(Math.abs(ativo.change) + 0.01);

                    const isPositive = ativo.change >= 0;
                    const changeSign = isPositive ? '+' : '';

                    let currency = "$";
                    if (ativo.symbol.endsWith('.SA') || ativo.symbol === 'BRL=X' || ativo.symbol === '^BVSP') {
                        currency = "R$";
                    }

                    // Custom text for the block
                    // Use Name from backend if available
                    const displayName = ativo.name || ativo.symbol;

                    texts.push(`<b>${displayName}</b><br><span style="font-size:0.8em">${ativo.symbol}</span><br>${currency} ${ativo.price.toFixed(2)}<br>${changeSign}${ativo.change.toFixed(2)}%`);

                    // Color logic
                    if (isPositive) {
                        // Green scale
                        colors.push('#10b981');
                    } else {
                        // Red scale
                        colors.push('#ef4444');
                    }
                });

                const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
                const textColor = '#ffffff'; // Always white text inside blocks
                const textColors = [];

                // Populate colors for assets
                dados.forEach(() => {
                    textColors.push(textColor);
                });

                // Add Root Node
                labels.push(rootLabel);
                parents.push("");
                values.push(0);
                texts.push("");
                colors.push("transparent");

                // Color for root node label
                // If dark mode, match background (#112240) to hide it. Else white.
                if (isDark) {
                    textColors.push('#112240');
                } else {
                    textColors.push(textColor);
                }


                const data = [{
                    type: "treemap",
                    labels: labels,
                    parents: parents,
                    values: values,
                    text: texts,
                    textinfo: "text",
                    hoverinfo: "label+text+value",
                    pathbar: { visible: false }, // Hide the top bar "Mercado"
                    marker: {
                        colors: colors,
                        line: { width: 1, color: isDark ? '#112240' : '#ffffff' }
                    },
                    textfont: {
                        family: 'Manrope, sans-serif',
                        size: 14,
                        color: textColors,
                        weight: 700
                    },
                    tiling: {
                        packing: 'squarify' // 'squarify', 'binary', 'dice', 'slice', 'slice-dice', 'dice-slice'
                    }
                }];

                const layout = {
                    margin: { t: 0, l: 0, r: 0, b: 0 },
                    paper_bgcolor: 'transparent',
                    font: { family: 'Manrope, sans-serif' }
                };

                Plotly.newPlot('heatmap-plot', data, layout, { responsive: true, displayModeBar: false });



            } catch (e) {
                console.error("Erro heatmap:", e);
                const errorMsg = (window.translations && window.translations[currentLang] && window.translations[currentLang].heatmap_error) 
                                 ? window.translations[currentLang].heatmap_error 
                                 : "Erro ao carregar mercado<br>Recarregue a página";
                document.getElementById('heatmap-plot').innerHTML = `<div style="text-align: center; padding: 50px; color: red; font-family: sans-serif;">${errorMsg}</div>`;
            } finally {
                // Hide loader
                if (loader) loader.classList.remove('active');
            }
        }

        // --- Chart Logic ---
        async function mudouAtivo() {
            toggleSpinner('chart-spinner', true);

            const ativoSelecionado = document.getElementById('ativo-atual').value;
            const periodo = document.getElementById('seletor-periodo').value;
            const intervalo = document.getElementById('seletor-intervalo').value;
            const maPeriod = document.getElementById('input-ma').value;
            const showRSI = document.getElementById('check-rsi').checked;
            const showMACD = document.getElementById('check-macd').checked;
            const showStoch = document.getElementById('check-stoch').checked;
            const showVol = document.getElementById('check-vol').checked;
            const showATR = document.getElementById('check-atr').checked;
            const checkMaEl = document.getElementById('check-ma');
            const showMA = checkMaEl ? checkMaEl.checked : true; // Default to true if not found

            try {
                const response = await fetch(`${API_BASE_URL}/api/dados?ticker=${ativoSelecionado}&period=${periodo}&interval=${intervalo}&ma_period=${maPeriod}`);
                if (!response.ok) throw new Error("Erro na API");
                const dados = await response.json();

                document.getElementById('titulo-ativo').innerText = dados.symbol;

                let currencySymbol = "$";
                if (dados.symbol.endsWith('.SA') || dados.symbol === 'BRL=X' || dados.symbol === '^BVSP') {
                    currencySymbol = "R$";
                }
                const precoEl = document.getElementById('preco');
                precoEl.innerText = `${currencySymbol} ${dados.preco_atual}`;

                const traces = [];

                // Main Candle Trace
                traces.push({
                    x: dados.datas,
                    close: dados.close,
                    decreasing: { line: { color: '#d32f2f', width: 1 } },
                    high: dados.high,
                    increasing: { line: { color: '#008000', width: 1 } },
                    low: dados.low,
                    open: dados.open,
                    type: 'candlestick',
                    name: (window.translations && window.translations[currentLang] && window.translations[currentLang].chart_price) || 'Preço'
                });

                // Moving Average Trace
                if (showMA) {
                    traces.push({
                        x: dados.datas,
                        y: dados.ma,
                        type: 'scatter',
                        mode: 'lines',
                        line: { color: getComputedStyle(document.documentElement).getPropertyValue('--accent-primary').trim(), width: 1.5 },
                        name: dados.ma_label
                    });
                }

                const layout = {
                    ...getPlotLayout(),
                    dragmode: 'pan',
                    showlegend: false,
                    xaxis: {
                        ...getPlotLayout().xaxis,
                        type: 'date',
                        rangeslider: { visible: false },
                        anchor: 'free',
                        position: 0
                    }
                };

                // --- Smart Tick Generation Logic ---
                // Identify target number of ticks
                const targetTicks = 8;
                const len = dados.datas.length;
                const step = Math.max(1, Math.floor(len / targetTicks));

                const tickVals = [];
                const tickText = [];

                for (let i = 0; i < len; i += step) {
                    tickVals.push(dados.datas[i]); // In category axis, the value is the category name itself (the date string)

                    // Format Label
                    const dateObj = new Date(dados.datas[i]);
                    let label = "";

                    if (periodo.includes('d') || periodo.includes('wk') || periodo.includes('mo')) {
                        // Daily/Weekly: "DD MMM" (e.g., "14 Nov")
                        const day = dateObj.getDate();
                        const month = dateObj.toLocaleDateString(currentLang === 'pt' ? 'pt-BR' : 'en-US', { month: 'short' });
                        // Remove dot from month if present
                        label = `${day} ${month.replace('.', '')}`;
                    } else if (periodo.includes('1d') || intervalo.includes('m') || intervalo.includes('h')) {
                        // Intraday: "HH:mm" (e.g., "14:30") 
                        // For longer intraday periods, might need date too
                        if (periodo === '1d' || periodo === '5d') {
                            const hours = String(dateObj.getHours()).padStart(2, '0');
                            const mins = String(dateObj.getMinutes()).padStart(2, '0');
                            const day = dateObj.getDate();
                            if (periodo === '5d') {
                                label = `${day} - ${hours}:${mins}`;
                            } else {
                                label = `${hours}:${mins}`;
                            }
                        } else {
                            // Default fallback
                            const day = dateObj.getDate();
                            const month = dateObj.toLocaleDateString(currentLang === 'pt' ? 'pt-BR' : 'en-US', { month: 'short' });
                            label = `${day} ${month.replace('.', '')}`;
                        }
                    } else {
                        // Default
                        const day = dateObj.getDate();
                        const month = dateObj.toLocaleDateString(currentLang === 'pt' ? 'pt-BR' : 'en-US', { month: 'short' });
                        label = `${day} ${month.replace('.', '')}`;
                    }
                    tickText.push(label);
                }

                // Standardize ALL charts (Crypto + Stocks) to use Category axis with CUSTOM TICKS.
                layout.xaxis.type = 'category';
                layout.xaxis.tickmode = 'array'; // Manual ticks
                layout.xaxis.tickvals = tickVals;
                layout.xaxis.ticktext = tickText;
                // layout.xaxis.nticks is ignored when tickmode is array






                // Dynamic Layout Logic for Indicators
                const indicators = [];
                if (showRSI) indicators.push('rsi');
                if (showMACD) indicators.push('macd');
                if (showStoch) indicators.push('stoch');
                if (showVol) indicators.push('vol');
                if (showATR) indicators.push('atr');

                const numIndicators = indicators.length;
                let mainDomain = [0.1, 1];

                if (numIndicators === 0) {
                    mainDomain = [0, 1];
                } else if (numIndicators === 1) {
                    mainDomain = [0.3, 1];
                } else if (numIndicators === 2) {
                    mainDomain = [0.45, 1];
                } else if (numIndicators === 3) {
                    mainDomain = [0.55, 1];
                } else if (numIndicators === 4) {
                    mainDomain = [0.60, 1];
                } else if (numIndicators === 5) {
                    mainDomain = [0.65, 1];
                }

                layout.yaxis.domain = mainDomain;

                // Helper to get domain for a specific slot index (0 = bottom)
                function getDomain(idx, total) {
                    // Simple uniform distribution for up to 5 indicators
                    // Reserved height for indicators: 1 - mainDomain[0] (approx)
                    // Wait, mainDomain starts at X. Indicators are below X.
                    // E.g. 1 indicator: Main 0.3-1. Indicator 0-0.2.
                    
                    // Let's refine for up to 5 slots
                    const slotHeight = 0.85 / Math.max(total * 1.5 + 2, 4); // Adaptive height
                    // This logic is getting complex, let's stick to the previous hardcoded style but extend it
                    
                    if (total === 5) {
                        const h = 0.10; // height per plot
                        const g = 0.03; // gap
                        const start = idx * (h + g);
                        return [start, start + h];
                    }
                    
                    if (total === 1) return [0, 0.2];
                    if (total === 2) {
                        if (idx === 0) return [0, 0.2];
                        if (idx === 1) return [0.25, 0.40];
                    }
                    if (total === 3) {
                        return [idx * 0.18, idx * 0.18 + 0.13]; // Approx logic
                    }
                    if (total === 4) {
                        return [idx * 0.14, idx * 0.14 + 0.10];
                    }
                     return [0, 0.2];
                }

                // Assign slots based on fixed priority: 
                // ATR -> Vol -> Stoch -> MACD -> RSI (Bottom to Top ?)
                // Let's map dynamically
                const activeTypes = [];
                if (showRSI) activeTypes.push('rsi');
                if (showMACD) activeTypes.push('macd');
                if (showStoch) activeTypes.push('stoch');
                if (showVol) activeTypes.push('vol');
                if (showATR) activeTypes.push('atr');
                
                // Reverse to stack from bottom up?
                // reversedTypes[0] will be at bottom slot (idx 0)
                const reversedTypes = [...activeTypes].reverse();



                // --- RSI Logic ---
                if (showRSI && dados.rsi) {
                    const slotIndex = reversedTypes.indexOf('rsi');
                    const rsiDomain = getDomain(slotIndex, numIndicators);

                    layout.yaxis2 = {
                        domain: rsiDomain,
                        range: [0, 100],
                        gridcolor: layout.yaxis.gridcolor,
                        fixedrange: true,
                        tickfont: layout.yaxis.tickfont
                    };

                    // RSI Trace
                    traces.push({
                        x: dados.datas,
                        y: dados.rsi,
                        type: 'scatter',
                        mode: 'lines',
                        line: { color: '#9c27b0', width: 1.5 },
                        name: 'RSI',
                        yaxis: 'y2'
                    });

                    // Overbought/Oversold Lines
                    const lineStyle = { color: 'rgba(128,128,128,0.5)', width: 1, dash: 'dash' };
                    traces.push({
                        x: [dados.datas[0], dados.datas[dados.datas.length - 1]],
                        y: [70, 70],
                        type: 'scatter',
                        mode: 'lines',
                        line: lineStyle,
                        showlegend: false,
                        hoverinfo: 'none',
                        yaxis: 'y2'
                    });
                    traces.push({
                        x: [dados.datas[0], dados.datas[dados.datas.length - 1]],
                        y: [30, 30],
                        type: 'scatter',
                        mode: 'lines',
                        line: lineStyle,
                        showlegend: false,
                        hoverinfo: 'none',
                        yaxis: 'y2'
                    });
                }




                // --- MACD Logic ---
                if (showMACD && dados.macd) {
                    const slotIndex = reversedTypes.indexOf('macd');
                    const macdDomain = getDomain(slotIndex, numIndicators);

                    // MACD Axis
                    layout.yaxis3 = {
                        domain: macdDomain,
                        gridcolor: layout.yaxis.gridcolor,
                        fixedrange: true,
                        tickfont: layout.yaxis.tickfont
                    };


                    const colors = {
                        macd: '#2962FF',
                        signal: '#FF6D00',
                        histUp: '#26A69A',
                        histDown: '#EF5350'
                    };

                    // MACD Histogram
                    traces.push({
                        x: dados.datas,
                        y: dados.macd_hist,
                        type: 'bar',
                        name: 'Histograma',
                        marker: {
                            color: dados.macd_hist.map(v => v >= 0 ? colors.histUp : colors.histDown)
                        },
                        yaxis: 'y3'
                    });

                    // MACD Line
                    traces.push({
                        x: dados.datas,
                        y: dados.macd,
                        type: 'scatter',
                        mode: 'lines',
                        line: { color: colors.macd, width: 1.5 },
                        name: 'MACD',
                        yaxis: 'y3'
                    });

                    // Signal Line
                    traces.push({
                        x: dados.datas,
                        y: dados.signal,
                        type: 'scatter',
                        mode: 'lines',
                        line: { color: colors.signal, width: 1.5 },
                        name: 'Sinal',
                        yaxis: 'y3'
                    });
                }

                // --- Stochastic Logic ---
                if (showStoch && dados.stoch_k) {
                    const slotIndex = reversedTypes.indexOf('stoch');
                    const stochDomain = getDomain(slotIndex, numIndicators);

                    layout.yaxis4 = {
                        domain: stochDomain,
                        gridcolor: layout.yaxis.gridcolor,
                        fixedrange: true,
                        range: [0, 100],
                        tickfont: layout.yaxis.tickfont
                    };

                    traces.push({
                        x: dados.datas,
                        y: dados.stoch_k,
                        type: 'scatter',
                        mode: 'lines',
                        line: { color: '#00B0FF', width: 1.5 },
                        name: '%K',
                        yaxis: 'y4'
                    });
                    traces.push({
                        x: dados.datas,
                        y: dados.stoch_d,
                        type: 'scatter',
                        mode: 'lines',
                        line: { color: '#FF4081', width: 1.5 },
                        name: '%D',
                        yaxis: 'y4'
                    });

                    // Bands
                    const lineStyle = { color: 'rgba(128,128,128,0.3)', width: 1, dash: 'dot' };
                    traces.push({
                        x: [dados.datas[0], dados.datas[dados.datas.length-1]], y: [80, 80], type: 'scatter', mode: 'lines', line: lineStyle, showlegend: false, hoverinfo: 'none', yaxis: 'y4'
                    });
                    traces.push({
                        x: [dados.datas[0], dados.datas[dados.datas.length-1]], y: [20, 20], type: 'scatter', mode: 'lines', line: lineStyle, showlegend: false, hoverinfo: 'none', yaxis: 'y4'
                    });
                }

                // --- Volume Logic ---
                if (showVol && dados.volume) {
                    const slotIndex = reversedTypes.indexOf('vol');
                    const volDomain = getDomain(slotIndex, numIndicators);

                    layout.yaxis5 = {
                        domain: volDomain,
                        gridcolor: layout.yaxis.gridcolor,
                        fixedrange: true,
                        tickfont: layout.yaxis.tickfont
                    };

                    const colors = dados.close.map((c, i) => {
                        if (i === 0) return '#26A69A';
                        return c >= dados.close[i - 1] ? '#26A69A' : '#EF5350';
                    });

                    traces.push({
                        x: dados.datas,
                        y: dados.volume,
                        type: 'bar',
                        name: 'Volume',
                        marker: {
                            color: colors
                        },
                        yaxis: 'y5'
                    });
                }

                // --- ATR Logic ---
                if (showATR && dados.atr) {
                    const slotIndex = reversedTypes.indexOf('atr');
                    const atrDomain = getDomain(slotIndex, numIndicators);

                    layout.yaxis6 = {
                        domain: atrDomain,
                        gridcolor: layout.yaxis.gridcolor,
                        fixedrange: true,
                        tickfont: layout.yaxis.tickfont,
                        title: { text: 'ATR', font: { size: 10, color: 'var(--text-muted)' } }
                    };

                    traces.push({
                        x: dados.datas,
                        y: dados.atr,
                        type: 'scatter',
                        mode: 'lines',
                        line: { color: '#FFD700', width: 1.5 }, // Gold color
                        name: 'ATR (14)',
                        yaxis: 'y6'
                    });
                }

                Plotly.newPlot('grafico', traces, layout, { responsive: true, displayModeBar: false, scrollZoom: true });

            } catch (error) {
                console.error("Erro ao carregar dados:", error);
                toggleSpinner('chart-spinner', false);
            } finally {
                toggleSpinner('chart-spinner', false);
            }
        }

        // --- Market Movers Logic ---
        async function loadMarketMovers() {
            const listGainers = document.getElementById('gainers-list');
            const listLosers = document.getElementById('losers-list');

            try {
                const category = document.getElementById('mover-category-select').value;
                const response = await fetch(`${API_BASE_URL}/api/market-movers?type=${category}`);
                if (!response.ok) throw new Error("API Error");
                const data = await response.json();

                renderMoverList('gainers-list', data.gainers);
                renderMoverList('losers-list', data.losers);

            } catch (e) {
                console.error("Erro loading movers:", e);
                const retryText = (window.translations && window.translations[currentLang] && window.translations[currentLang].heatmap_error) 
                                 ? (currentLang === 'en' ? 'Reload' : 'Recarregar') 
                                 : 'Recarregar';
                const errorText = (window.translations && window.translations[currentLang] && window.translations[currentLang].error_loading) 
                                 ? window.translations[currentLang].error_loading 
                                 : 'Erro ao carregar dados.';
                                 
                const retryBtn = `<button onclick="loadMarketMovers()" style="background:none; border:none; color:var(--accent-primary); cursor:pointer; text-decoration:underline;">${retryText}</button>`;
                const errorHtml = `<li class="mover-item" style="color:var(--text-muted); justify-content:center; flex-direction:column;">
                                    <span>${errorText}</span>
                                    ${retryBtn}
                                   </li>`;

                if (listGainers) listGainers.innerHTML = errorHtml;
                if (listLosers) listLosers.innerHTML = errorHtml;
            }
        }

        function renderMoverList(elementId, items) {
            const list = document.getElementById(elementId);
            if (!list) return;
            list.innerHTML = '';

            items.forEach(item => {
                const li = document.createElement('li');
                li.className = 'mover-item';

                const changeClass = item.change >= 0 ? 'change-positive' : 'change-negative';
                const sign = item.change >= 0 ? '+' : '';

                // Name Logic: Use name if available, else symbol
                // Prioritize Name as main display
                const displayName = item.name || item.symbol;

                li.innerHTML = `
            <div style="display:flex; flex-direction:column;">
                <span class="mover-symbol" style="font-size:14px;">${displayName}</span>
                ${item.name ? `<span style="font-size:11px; color:var(--text-muted);">${item.symbol}</span>` : ''}
            </div>
            <div>
                <span class="mover-price">$${item.price.toFixed(2)}</span>
                <span class="mover-change ${changeClass}">${sign}${item.change.toFixed(2)}%</span>
            </div>
        `;
                list.appendChild(li);
            });
        }

        // Inicialização
        document.addEventListener('DOMContentLoaded', () => {
            loadTheme();

            // Mobile specific defaults: Set chart period to 3 Months
            if (window.innerWidth <= 768) {
                const periodoSelect = document.getElementById('seletor-periodo');
                if (periodoSelect) {
                    periodoSelect.value = '3mo';
                }
            }

            fetchAssets();
            setupAutocomplete();
            carregarHeatmap();
            mudouAtivo();
            loadMarketMovers();

            setInterval(() => mudouAtivo(), 60000);
            // setInterval(() => carregarListaLateral(), 60000); // Removed
            setInterval(() => carregarHeatmap(), 60000);
            setInterval(() => loadMarketMovers(), 60000);
        });
