const translations = {
    pt: {
        // Nav
        nav_home: "Início",
        nav_platform: "Plataforma",
        nav_market: "Mercado",
        nav_analysis: "Análise",
        nav_risk: "Correlação & Risco",
        nav_portfolio: "Gerenciar Portfólio",
        nav_hello: "Olá",
        nav_logout: "Sair",
        nav_login_reg: "Entrar / Registrar",
        
        // Hero
        hero_title_part1: "O futuro das finanças",
        hero_title_part2: "precisa de clareza.",
        hero_subtitle: "Monitore o mercado global em tempo real com a precisão que você precisa para tomar as melhores decisões.",
        hero_cta: "Acessar Plataforma",
        
        // Dashboard
        dash_title: "FinSense Dashboard",
        controls_candles: "Quantidade de Velas",
        controls_time: "Tempo",
        controls_indicators: "Indicadores",
        controls_select: "Selecionar...",
        controls_ma: "Média Móvel",
        controls_rsi: "RSI",
        controls_macd: "MACD",
        controls_stoch: "Estocástico",
        controls_vol: "Volume",
        search_placeholder: "Buscar ativo (ex: PETR4)...",
        
        // Market Movers / Sidebar
        movers_title: "Destaques do Mercado",
        movers_gainers: "Maiores Altas (Top 5)",
        movers_losers: "Maiores Baixas (Top 5)",
        movers_loading: "Carregando...",
        cat_crypto: "Criptomoedas",
        cat_br: "Ações Brasil",
        cat_us: "Ações EUA",
        cat_indices: "Índices",
        cat_all: "Todos",
        cat_indices_global: "Índices Globais",
        cat_all_cats: "Todas as Categorias",

        // Analise Carteiras
        analysis_title: "Análise de Carteiras",
        analysis_subtitle: "Analise a correlação entre os ativos da sua carteira para entender melhor a diversificação e o risco.",
        config_title: "Configuração da Carteira",
        sel_assets: "1. Seleção de Ativos",
        no_assets: "Nenhum ativo selecionado.",
        sel_period: "2. Período da Análise",
        date_start: "Início",
        date_end: "Fim",
        risk_corr_title: "Risco & Correlação",
        risk_corr_desc: "Matriz de correlação e análise de diversificação.",
        btn_analyze: "Analisar",
        benchmark_title: "Benchmark",
        btn_compare: "Comparar",
        res_corr_summary: "Resumo da Correlação",
        res_avg_corr: "Média de Correlação Absoluta",
        res_perf_comp: "Comparação de Rentabilidade: Carteira vs Benchmark",
        res_note: "* A curva 'Minha Carteira' é calculada com base nos pesos definidos acima.",
        processing: "Processando Dados...",
        
        // Portfolio
        my_portfolio: "Minha Carteira", // If needed
        pf_total_balance: "Saldo Total",
        pf_total_invested: "Total Investido",
        pf_total_profit: "Lucro/Prejuízo",
        pf_add_asset: "Adicionar Ativo",
        pf_ticker: "Ticker",
        pf_qty: "Quantidade",
        pf_avg_price: "Preço Médio",
        btn_add: "Adicionar",
        btn_calc_total: "Calcular Totais",
        tbl_asset: "Ativo",
        tbl_qty: "Qtd",
        tbl_avg_price: "Preço Médio",
        tbl_current_price: "Preço Atual",
        tbl_total_val: "Valor Total",
        tbl_pl: "Lucro/Prej",
        tbl_action: "Ação",
        
        // Login
        login_subtitle: "Acesse sua carteira inteligente",
        login_create_title: "Crie sua conta gratuita",
        lbl_user: "Usuário",
        lbl_pass: "Senha",
        ph_user: "Digite seu usuário",
        ph_pass: "Digite sua senha",
        btn_enter: "Entrar",
        btn_create: "Criar Conta",
        txt_no_account: "Não tem uma conta?",
        txt_have_account: "Já tem uma conta?",
        link_register: "Registrar-se",
        link_login: "Entrar",

        // Portfolio Specific
        filter_br: "Brasil",
        filter_us: "EUA",
        filter_crypto: "Cripto",
        chart_alloc: "Alocação da Carteira",
        chart_evol: "Evolução Patrimonial",
        chart_hist: "Histórico de Transações",
        tx_new: "Nova Transação",
        lbl_date_buy: "Data da Compra",
        lbl_price_unit: "Preço Unitário",
        btn_calc_rent: "Calcular Rentabilidade",
        th_date: "Data",
        th_total: "Total",
        empty_tx: "Nenhuma transação adicionada.",

        // Modal & Heatmap
        modal_title: "Acesso Restrito",
        modal_body: "Você precisa estar logado para acessar os recursos avançados da plataforma.",
        modal_cancel: "Cancelar",
        modal_login: "Fazer Login",
        heatmap_title: "Mapa de Mercado",
        heatmap_loading: "Carregando Mercado...",
        heatmap_error: "Erro ao carregar mercado<br>Recarregue a página",
        error_loading: "Erro ao carregar dados.",
        sidebar_loading: "Carregando preços...",
        chart_price: "Preço",
        chart_volume: "Volume",
        chart_error: "Erro ao carregar",
        
        // Analysis Results
        corr_high: "ALTA",
        corr_mod: "MODERADA",
        corr_low: "BAIXA OU DESCORRELACIONADA",
        corr_desc_high: "Isso indica que seus ativos tendem a se mover na mesma direção, o que reduz os benefícios da diversificação. Em momentos de crise, é provável que a maioria sofra quedas simultâneas, aumentando o risco sistêmico da carteira.",
        corr_desc_mod: "Isso indica que existe algum nível de diversificação, mas os ativos ainda podem sofrer influências de mercado similares. É um ponto de equilíbrio, mas vale considerar adicionar ativos descorrelacionados para maior proteção.",
        corr_desc_low: "Isso significa que os ativos comportam-se de maneira independente ou até inversa. Na gestão de carteiras, esta é uma configuração favorável para mitigar o risco não-sistêmico (idiossincrático). Seus ativos oferecem proteção real uns aos outros, estabilizando a curva de capital da carteira no longo prazo.",
        corr_intro_1: "O Coeficiente de Correlação de Pearson Médio de",
        corr_intro_2: "desta carteira indica uma correlação",
        
        bench_win: "Sua Carteira superou o Benchmark!",
        bench_loss: "O Benchmark superou sua Carteira.",
        bench_summary_1: "No período analisado, sua carteira rendeu",
        bench_summary_2: "enquanto o",
        bench_summary_3: "rendeu",
        bench_diff: "Uma diferença de",
        bench_equiv: "(Equivalente)",
        
        // Errors
        error_min_assets_corr: "Insira pelo menos 2 ativos para calcular correlação.",
        error_min_assets_bench: "Insira pelo menos 1 ativo para o benchmark.",
        error_select_dates: "Por favor, selecione as datas.",
        error_prefix: "Erro: ",
        
        // Portfolio Loading
        alloc_loading: "Carregando alocação...",
        calc_rent_loading: "Calculando Rentabilidade...",
        
        // Login Errors
        error_auth: "Erro na autenticação",
        error_connection: "Erro de conexão com o servidor. Verifique se o app.py está rodando.",
        btn_processing: "Processando...",
        
        // Timeframes
        tf_1d: "1 Dia",
        tf_5d: "5 Dias",
        tf_1m: "1 Mês",
        tf_3m: "3 Meses",
        tf_6m: "6 Meses",
        tf_1y: "1 Ano",
        tf_max: "Máx",
        tf_15m: "15 Min",
        tf_30m: "30 Min",
        tf_1h: "1 Hora",
        tf_1w: "1 Sem"
    },
    en: {
        // Nav
        nav_home: "Home",
        nav_platform: "Platform",
        nav_market: "Market",
        nav_analysis: "Analysis",
        nav_risk: "Correlation & Risk",
        nav_portfolio: "Manage Portfolio",
        nav_hello: "Hello",
        nav_logout: "Logout",
        nav_login_reg: "Login / Register",
        
        // Hero
        hero_title_part1: "The future of finance",
        hero_title_part2: "needs clarity.",
        hero_subtitle: "Monitor the global market in real-time with the precision you need to make the best decisions.",
        hero_cta: "Access Platform",
        
        // Dashboard
        dash_title: "FinSense Dashboard",
        controls_candles: "Candles Count",
        controls_time: "Timeframe",
        controls_indicators: "Indicators",
        controls_select: "Select...",
        controls_ma: "Moving Average",
        controls_rsi: "RSI",
        controls_macd: "MACD",
        controls_stoch: "Stochastic",
        controls_vol: "Volume",
        search_placeholder: "Search asset (e.g. PETR4)...",
        
        // Market Movers / Sidebar
        movers_title: "Market Highlights",
        movers_gainers: "Top Gainers (Top 5)",
        movers_losers: "Top Losers (Top 5)",
        movers_loading: "Loading...",
        cat_crypto: "Cryptocurrencies",
        cat_br: "Brazil Stocks",
        cat_us: "US Stocks",
        cat_indices: "Indices",
        cat_all: "All",
        cat_indices_global: "Global Indices",
        cat_all_cats: "All Categories",

        // Analise Carteiras
        analysis_title: "Portfolio Analysis",
        analysis_subtitle: "Analyze the correlation between assets in your portfolio to better understand diversification and risk.",
        config_title: "Portfolio Configuration",
        sel_assets: "1. Asset Selection",
        no_assets: "No assets selected.",
        sel_period: "2. Analysis Period",
        date_start: "Start",
        date_end: "End",
        risk_corr_title: "Risk & Correlation",
        risk_corr_desc: "Correlation matrix and diversification analysis.",
        btn_analyze: "Analyze",
        benchmark_title: "Benchmark",
        btn_compare: "Compare",
        res_corr_summary: "Correlation Summary",
        res_avg_corr: "Average Absolute Correlation",
        res_perf_comp: "Profitability Comparison: Portfolio vs Benchmark",
        res_note: "* The 'My Portfolio' curve is calculated based on the weights defined above.",
        processing: "Processing Data...",
        
        // Portfolio
        my_portfolio: "My Portfolio",
        pf_total_balance: "Total Balance",
        pf_total_invested: "Total Invested",
        pf_total_profit: "Profit/Loss",
        pf_add_asset: "Add Asset",
        pf_ticker: "Ticker",
        pf_qty: "Quantity",
        pf_avg_price: "Avg Price",
        btn_add: "Add",
        btn_calc_total: "Calculate Totals",
        tbl_asset: "Asset",
        tbl_qty: "Qty",
        tbl_avg_price: "Avg Price",
        tbl_current_price: "Current Price",
        tbl_total_val: "Total Value",
        tbl_pl: "Profit/Loss",
        tbl_action: "Action",
        
        // Login
        login_subtitle: "Access your smart portfolio",
        login_create_title: "Create your free account",
        lbl_user: "Username",
        lbl_pass: "Password",
        ph_user: "Enter your username",
        ph_pass: "Enter your password",
        btn_enter: "Login",
        btn_create: "Create Account",
        txt_no_account: "Don't have an account?",
        txt_have_account: "Already have an account?",
        link_register: "Register",
        link_login: "Login",

        // Portfolio Specific
        filter_br: "Brazil",
        filter_us: "USA",
        filter_crypto: "Crypto",
        chart_alloc: "Portfolio Allocation",
        chart_evol: "Portfolio Performance",
        chart_hist: "Transaction History",
        tx_new: "New Transaction",
        lbl_date_buy: "Purchase Date",
        lbl_price_unit: "Unit Price",
        btn_calc_rent: "Calculate Returns",
        th_date: "Date",
        th_total: "Total",
        th_total: "Total",
        empty_tx: "No transactions added.",

        // Modal & Heatmap
        modal_title: "Restricted Access",
        modal_body: "You need to be logged in to access the platform's advanced features.",
        modal_cancel: "Cancel",
        modal_login: "Login",
        heatmap_title: "Market Map",
        heatmap_loading: "Loading Market...",
        heatmap_error: "Error loading market<br>Reload page",
        error_loading: "Error loading data.",
        sidebar_loading: "Loading prices...",
        chart_price: "Price",
        chart_volume: "Volume",
        chart_error: "Error loading",
        
        // Analysis Results
        corr_high: "HIGH",
        corr_mod: "MODERATE",
        corr_low: "LOW OR UNCORRELATED",
        corr_desc_high: "This indicates that your assets tend to move in the same direction, reducing diversification benefits. In moments of crisis, most may suffer simultaneous drops, increasing the portfolio's systemic risk.",
        corr_desc_mod: "This indicates some level of diversification, but assets may still suffer similar market influences. It's a balance point, but consider adding uncorrelated assets for greater protection.",
        corr_desc_low: "This means assets behave independently or even inversely. In portfolio management, this is a favorable setup to mitigate non-systemic (idiosyncratic) risk. Your assets offer real protection to each other, stabilizing the capital curve in the long run.",
        corr_intro_1: "The Average Pearson Correlation Coefficient of",
        corr_intro_2: "of this portfolio indicates a correlation",
        
        bench_win: "Your Portfolio beat the Benchmark!",
        bench_loss: "The Benchmark beat your Portfolio.",
        bench_summary_1: "In the analyzed period, your portfolio returned",
        bench_summary_2: "while the",
        bench_summary_3: "returned",
        bench_diff: "A difference of",
        bench_equiv: "(Equivalent)",
        
        // Errors
        error_min_assets_corr: "Enter at least 2 assets to calculate correlation.",
        error_min_assets_bench: "Enter at least 1 asset for the benchmark.",
        error_select_dates: "Please select dates.",
        error_prefix: "Error: ",
        
        // Portfolio Loading
        alloc_loading: "Loading allocation...",
        calc_rent_loading: "Calculating Returns...",
        
        // Login Errors
        error_auth: "Authentication error",
        error_connection: "Server connection error. Check if app.py is running.",
        btn_processing: "Processing...",
        
        // Timeframes
        tf_1d: "1 Day",
        tf_5d: "5 Days",
        tf_1m: "1 Month",
        tf_3m: "3 Months",
        tf_6m: "6 Months",
        tf_1y: "1 Year",
        tf_max: "Max",
        tf_15m: "15 Min",
        tf_30m: "30 Min",
        tf_1h: "1 Hour",
        tf_1w: "1 Week"
    }
};


window.translations = translations;
window.currentLang = localStorage.getItem('lang') || 'pt';

function updateLanguage(lang) {
    if (!translations[lang]) return;
    window.currentLang = lang; // Update global
    localStorage.setItem('lang', lang);

    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang][key]) {
            // Check if it's an input with placeholder
            if (el.tagName.toUpperCase() === 'INPUT' && el.hasAttribute('placeholder')) {
                el.placeholder = translations[lang][key];
            } else {
                el.textContent = translations[lang][key];
            }
        }
    });
    
// Update button flag/text if exists
    const btn = document.getElementById('lang-toggle');
    if (btn) {
        btn.innerHTML = lang === 'pt' ? '🇺🇸' : '🇧🇷'; 
        btn.title = lang === 'pt' ? 'Switch to English' : 'Mudar para Português';
    }

    // Dispatch event for dynamic content
    window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang: lang } }));
}

function toggleLanguage() {
    const newLang = window.currentLang === 'pt' ? 'en' : 'pt';
    updateLanguage(newLang);
}

// Auto-init on load
document.addEventListener('DOMContentLoaded', () => {
    updateLanguage(currentLang);
});
