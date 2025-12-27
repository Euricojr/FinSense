const translations = {
  pt: {
    // Nav
    nav_home: "Início",
    nav_platform: "Plataforma",
    nav_market: "Mercado",
    nav_analysis: "Análise",
    nav_risk: "Correlação & Risco",
    nav_simulations: "Simulações",
    nav_optimization: "Otimização Markowitz",
    nav_portfolio: "Gerenciar Portfólio",
    nav_hello: "Olá",
    nav_logout: "Sair",
    nav_login_reg: "Entrar / Registrar",

    // Hero
    hero_title_part1: "O futuro das finanças",
    hero_title_part2: "precisa de clareza.",
    hero_subtitle:
      "Monitore o mercado global em tempo real com a precisão que você precisa para tomar as melhores decisões.",
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
    analysis_subtitle:
      "Analise a correlação entre os ativos da sua carteira para entender melhor a diversificação e o risco.",
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
    res_note:
      "* A curva 'Minha Carteira' é calculada com base nos pesos definidos acima.",
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
    modal_body:
      "Você precisa estar logado para acessar os recursos avançados da plataforma.",
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
    corr_desc_high:
      "Isso indica que seus ativos tendem a se mover na mesma direção, o que reduz os benefícios da diversificação. Em momentos de crise, é provável que a maioria sofra quedas simultâneas, aumentando o risco sistêmico da carteira.",
    corr_desc_mod:
      "Isso indica que existe algum nível de diversificação, mas os ativos ainda podem sofrer influências de mercado similares. É um ponto de equilíbrio, mas vale considerar adicionar ativos descorrelacionados para maior proteção.",
    corr_desc_low:
      "Isso significa que os ativos comportam-se de maneira independente ou até inversa. Na gestão de carteiras, esta é uma configuração favorável para mitigar o risco não-sistêmico (idiossincrático). Seus ativos oferecem proteção real uns aos outros, estabilizando a curva de capital da carteira no longo prazo.",
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
    error_min_assets_corr:
      "Insira pelo menos 2 ativos para calcular correlação.",
    error_min_assets_bench: "Insira pelo menos 1 ativo para o benchmark.",
    error_select_dates: "Por favor, selecione as datas.",
    error_prefix: "Erro: ",

    // Portfolio Loading
    alloc_loading: "Carregando alocação...",
    calc_rent_loading: "Calculando Rentabilidade...",

    // Login Errors
    error_auth: "Erro na autenticação",
    error_connection:
      "Erro de conexão com o servidor. Verifique se o app.py está rodando.",
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
    tf_1w: "1 Sem",

    // Indicators
    controls_atr: "ATR",

    // Simulation
    sim_title: "Simulação de Monte Carlo",
    sim_ticker: "Ativo (Ticker)",
    sim_horizon: "Horizonte (Dias)",
    sim_sims: "Simulações",
    sim_exec: "Executar Simulação",
    sim_current: "Preço Atual",
    sim_mean: "Média Projetada",
    sim_opt: "Otimista (95%)",
    sim_pess: "Pessimista (5%)",
    sim_win: "Prob. Lucro",
    sim_desc:
      "<strong>Como interpretar:</strong> O gráfico mostra até 50 caminhos possíveis para o preço do ativo. A linha <strong style='color:#00ff88'>Verde (Média)</strong> é o cenário base. As linhas otimista e pessimista indicam o intervalo de confiança de 90%.",
    sim_results_title: "Resultados da Carteira",
    sim_tbl_asset: "Ativo",
    sim_tbl_price: "Preço Atual",
    sim_tbl_mean: "Média Projetada",
    sim_tbl_opt: "Otimista (95%)",
    sim_tbl_pess: "Pessimista (5%)",
    sim_tbl_win: "Prob. Lucro",
    sim_btn_view: "Ver Gráfico",
    sim_add_alert: "Adicione pelo menos um ativo.",
    sim_limit_alert: "Máximo de 10 ativos.",
    sim_loading: "Processando Simulações...",
    sim_error: "Erro na simulação",

    // Optimization
    opt_title: "Otimização de Portfólio (Markowitz)",
    opt_input_label: "Ativos para Otimização (Mín. 2)",
    opt_btn_optimize: "Otimizar Portfólio",
    opt_chart_ef: "Fronteira Eficiente (Risco x Retorno)",
    opt_chart_sharpe: "Carteira Max Sharpe Ratio",
    opt_chart_vol: "Carteira Mínima Volatilidade",
    opt_rec: "Recomendado",
    opt_cons: "Conservador",
    opt_exp_ret: "Retorno Esperado",
    opt_vol: "Volatilidade",
    opt_sharpe: "Sharpe Ratio",
    opt_vol: "Volatilidade",
    opt_sharpe: "Sharpe Ratio",
    opt_loading: "Calculando Fronteira Eficiente...",
    opt_loading: "Calculando Fronteira Eficiente...",
    opt_btn_apply: "Aplicar Pesos",
    opt_applied_alert: "Pesos aplicados com sucesso! (Simulação)",
    opt_random: "Portfólios Aleatórios",
    opt_axis_vol: "Volatilidade (Risco)",
    opt_random: "Portfólios Aleatórios",
    opt_axis_vol: "Volatilidade (Risco)",
    opt_axis_ret: "Retorno Esperado",
    opt_period_label: "Período Histórico",
    opt_period_1y: "1 Ano",
    opt_period_2y: "2 Anos",
    opt_period_3y: "3 Anos",
    opt_period_5y: "5 Anos",

    // Prediction
    pred_title: "Modelo de Predição",
    pred_subtitle:
      "Projeção avançada de preços utilizando Machine Learning. O algoritmo analisa padrões históricos e indicadores técnicos para estimar tendências futuras com base nos parâmetros selecionados.",
    pred_assets_label: "ATIVOS (TAGS)",
    pred_train_label: "TREINO (ANOS)",
    pred_horizon_label: "HORIZONTE: <span id='horizonValue'>7</span> DIAS",
    pred_btn_analyze: "Gerar Análise",
    pred_trend: "TENDÊNCIA",
    pred_accuracy: "PRECISÃO DO MODELO",
    pred_volatility: "VOLATILIDADE RECENTE",
    pred_sentiment: "Sentimento IA",
    pred_placeholder: "Ex: BTC-USD, PETR4.SA (Enter)",
    pred_year_suffix: "Anos",
    pred_chart_title: "Previsão",
    pred_chart_history: "Histórico",
    pred_chart_pred: "IA Predição",
    pred_chart_unc: "Incerteza (95%)",
    pred_gauge_title: "Sentimento IA",
    pred_footer_1:
      "* O modelo utiliza Random Forest Regressor treinado com indicadores técnicos (SMA, RSI, Volatilidade).",
    pred_footer_2:
      "* A área sombreada representa o intervalo de incerteza (95%).",
    nav_prediction: "Modelo de Predição",
    trend_up: "Alta",
    trend_down: "Baixa",
    trend_up: "Alta",
    trend_down: "Baixa",
    trend_neutral: "Lateral",
    nav_hello: "Olá",
    pred_chart_xaxis: "Data",
    pred_chart_yaxis: "Preço",

    // Finances (New)
    nav_fin_mng: "Gestão de Finanças",
    fin_title: "Gestão Financeira",
    fin_ai_ph: "Ex: Gastei 45 reais no almoço com cartão de crédito...",
    fin_btn_process: "Processar",
    fin_total_income: "Total Ganhos (Mês)",
    fin_total_exp: "Total Gastos (Mês)",
    fin_balance: "Saldo Atual",
    fin_budget_impact: "Impacto no Orçamento",
    fin_ai_insight: "Insight IA",
    fin_analyzing: "Analisando seus dados...",
    fin_new_entry: "Novo Lançamento",
    fin_type_exp: "Despesa",
    fin_type_inc: "Ganho",
    fin_lbl_desc: "Descrição",
    fin_ph_desc: "Descrição...",
    fin_lbl_val: "Valor (R$)",
    fin_lbl_cat: "Categoria",
    fin_lbl_date: "Data",
    fin_lbl_pay: "Método de Pagamento",
    fin_btn_save: "Salvar Lançamento",
    fin_chart_title: "Gastos por Categoria",
    fin_hist_title: "Histórico Recente",
    fin_th_date: "Data",
    fin_th_desc: "Descrição",
    fin_th_cat: "Categoria",
    fin_th_pay: "Pagamento",
    fin_th_val: "Valor",

    // Categories & Methods
    cat_food: "Alimentação",
    cat_transport: "Transporte",
    cat_leisure: "Lazer",
    cat_housing: "Moradia",
    cat_health: "Saúde",
    cat_salary: "Salário",
    cat_divs: "Dividendos",
    cat_sales: "Vendas",
    cat_others: "Outros",

    pay_credit: "Cartão de Crédito",
    pay_debit: "Cartão de Débito",
    pay_pix: "Pix / Transferência",
    pay_cash: "Dinheiro",
    pay_others: "Outros",
  },
  en: {
    // Nav
    nav_home: "Home",
    nav_platform: "Platform",
    nav_market: "Market",
    nav_analysis: "Analysis",
    nav_risk: "Correlation & Risk",
    nav_simulations: "Simulations",
    nav_optimization: "Markowitz Optimization",
    nav_portfolio: "Manage Portfolio",
    nav_hello: "Hello",
    nav_logout: "Logout",
    nav_login_reg: "Login / Register",

    // Hero
    hero_title_part1: "The future of finance",
    hero_title_part2: "needs clarity.",
    hero_subtitle:
      "Monitor the global market in real-time with the precision you need to make the best decisions.",
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
    analysis_subtitle:
      "Analyze the correlation between assets in your portfolio to better understand diversification and risk.",
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
    res_note:
      "* The 'My Portfolio' curve is calculated based on the weights defined above.",
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
    modal_body:
      "You need to be logged in to access the platform's advanced features.",
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
    corr_desc_high:
      "This indicates that your assets tend to move in the same direction, reducing diversification benefits. In moments of crisis, most may suffer simultaneous drops, increasing the portfolio's systemic risk.",
    corr_desc_mod:
      "This indicates some level of diversification, but assets may still suffer similar market influences. It's a balance point, but consider adding uncorrelated assets for greater protection.",
    corr_desc_low:
      "This means assets behave independently or even inversely. In portfolio management, this is a favorable setup to mitigate non-systemic (idiosyncratic) risk. Your assets offer real protection to each other, stabilizing the capital curve in the long run.",
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
    tf_1w: "1 Week",

    // Indicators
    controls_atr: "ATR",

    // Simulation
    sim_title: "Monte Carlo Simulation",
    sim_ticker: "Asset (Ticker)",
    sim_horizon: "Horizon (Days)",
    sim_sims: "Simulations",
    sim_exec: "Run Simulation",
    sim_current: "Current Price",
    sim_mean: "Projected Mean",
    sim_opt: "Optimistic (95%)",
    sim_pess: "Pessimistic (5%)",
    sim_win: "Win Prob.",
    sim_desc:
      "<strong>How to interpret:</strong> The chart shows up to 50 possible paths for the asset price. The <strong style='color:#00ff88'>Green Line (Mean)</strong> is the base case. Optimistic and pessimistic lines indicate the 90% confidence interval.",
    sim_results_title: "Portfolio Results",
    sim_tbl_asset: "Asset",
    sim_tbl_price: "Current Price",
    sim_tbl_mean: "Projected Mean",
    sim_tbl_opt: "Optimistic (95%)",
    sim_tbl_pess: "Pessimistic (5%)",
    sim_tbl_win: "Win Prob.",
    sim_btn_view: "View Chart",
    sim_add_alert: "Add at least one asset.",
    sim_limit_alert: "Maximum of 10 assets.",
    sim_loading: "Processing Simulations...",
    sim_error: "Simulation Error",

    // Optimization
    opt_title: "Portfolio Optimization (Markowitz)",
    opt_input_label: "Assets for Optimization (Min 2)",
    opt_btn_optimize: "Optimize Portfolio",
    opt_chart_ef: "Efficient Frontier (Risk vs Return)",
    opt_chart_sharpe: "Max Sharpe Ratio Portfolio",
    opt_chart_vol: "Min Volatility Portfolio",
    opt_rec: "Recommended",
    opt_cons: "Conservative",
    opt_exp_ret: "Expected Return",
    opt_vol: "Volatility",
    opt_sharpe: "Sharpe Ratio",
    opt_vol: "Volatility",
    opt_sharpe: "Sharpe Ratio",
    opt_loading: "Calculating Efficient Frontier...",
    opt_loading: "Calculating Efficient Frontier...",
    opt_btn_apply: "Apply Weights",
    opt_applied_alert: "Weights applied successfully! (Simulation)",
    opt_random: "Random Portfolios",
    opt_axis_vol: "Volatility (Risk)",
    opt_random: "Random Portfolios",
    opt_axis_vol: "Volatility (Risk)",
    opt_axis_ret: "Expected Return",
    opt_period_label: "Historical Period",
    opt_period_1y: "1 Year",
    opt_period_2y: "2 Years",
    opt_period_3y: "3 Years",
    opt_period_5y: "5 Years",

    // Prediction
    pred_title: "Prediction Model",
    pred_subtitle:
      "Advanced price projection using Machine Learning. The algorithm analyzes historical patterns and technical indicators to estimate future trends based on selected parameters.",
    pred_assets_label: "ASSETS (TAGS)",
    pred_train_label: "TRAINING (YEARS)",
    pred_horizon_label: "HORIZON: <span id='horizonValue'>7</span> DAYS",
    pred_btn_analyze: "Generate Analysis",
    pred_trend: "TREND",
    pred_accuracy: "MODEL ACCURACY",
    pred_volatility: "RECENT VOLATILITY",
    pred_sentiment: "AI Sentiment",
    pred_placeholder: "Ex: BTC-USD, MSFT (Enter)",
    pred_year_suffix: "Years",
    pred_chart_title: "Forecast",
    pred_chart_history: "History",
    pred_chart_pred: "AI Prediction",
    pred_chart_unc: "Uncertainty (95%)",
    pred_gauge_title: "AI Sentiment",
    pred_footer_1:
      "* The model uses Random Forest Regressor trained with technical indicators (SMA, RSI, Volatility).",
    pred_footer_2: "* The shaded area represents the 95% uncertainty interval.",
    nav_prediction: "Prediction Model",
    trend_up: "Up",
    trend_down: "Down",
    trend_up: "Up",
    trend_down: "Down",
    trend_neutral: "Sideways",
    nav_hello: "Hello",
    pred_chart_xaxis: "Date",
    pred_chart_yaxis: "Price",

    // Finances (New)
    nav_fin_mng: "Finance Management",
    fin_title: "Finance Management",
    fin_ai_ph: "Ex: Spent 45 on lunch with credit card...",
    fin_btn_process: "Process",
    fin_total_income: "Total Income (Month)",
    fin_total_exp: "Total Expenses (Month)",
    fin_balance: "Current Balance",
    fin_budget_impact: "Budget Impact",
    fin_ai_insight: "AI Insight",
    fin_analyzing: "Analyzing your data...",
    fin_new_entry: "New Entry",
    fin_type_exp: "Expense",
    fin_type_inc: "Income",
    fin_lbl_desc: "Description",
    fin_ph_desc: "Description...",
    fin_lbl_val: "Amount ($)",
    fin_lbl_cat: "Category",
    fin_lbl_date: "Date",
    fin_lbl_pay: "Payment Method",
    fin_btn_save: "Save Entry",
    fin_chart_title: "Expenses by Category",
    fin_hist_title: "Recent History",
    fin_th_date: "Date",
    fin_th_desc: "Description",
    fin_th_cat: "Category",
    fin_th_pay: "Payment",
    fin_th_val: "Amount",

    // Categories & Methods
    cat_food: "Food",
    cat_transport: "Transport",
    cat_leisure: "Leisure",
    cat_housing: "Housing",
    cat_health: "Health",
    cat_salary: "Salary",
    cat_divs: "Dividends",
    cat_sales: "Sales",
    cat_others: "Others",

    pay_credit: "Credit Card",
    pay_debit: "Debit Card",
    pay_pix: "Bank Transfer/Pix",
    pay_cash: "Cash",
    pay_others: "Others",
  },
};

window.translations = translations;
window.currentLang = localStorage.getItem("lang") || "pt";

function updateLanguage(lang) {
  if (!translations[lang]) return;
  window.currentLang = lang; // Update global
  localStorage.setItem("lang", lang);

  const elements = document.querySelectorAll("[data-i18n]");
  elements.forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (translations[lang][key]) {
      // Check if it's an input with placeholder
      if (
        el.tagName.toUpperCase() === "INPUT" &&
        el.hasAttribute("placeholder")
      ) {
        el.placeholder = translations[lang][key];
      } else {
        el.innerHTML = translations[lang][key];
      }
    }
  });

  // Update button flag/text if exists
  const btn = document.getElementById("lang-toggle");
  if (btn) {
    // Option Q style: Bold text code
    btn.innerHTML =
      lang === "pt"
        ? '<span style="font-weight:700; font-size:14px;">EN</span>'
        : '<span style="font-weight:700; font-size:14px;">PT</span>';
    btn.title = lang === "pt" ? "Switch to English" : "Mudar para Português";
  }

  // Dispatch event for dynamic content
  window.dispatchEvent(
    new CustomEvent("languageChanged", { detail: { lang: lang } })
  );
}

function toggleLanguage() {
  const newLang = window.currentLang === "pt" ? "en" : "pt";
  updateLanguage(newLang);
}

// Auto-init on load
document.addEventListener("DOMContentLoaded", () => {
  updateLanguage(currentLang);
});

// Explicitly export to window to ensure availability
window.updateLanguage = updateLanguage;
window.toggleLanguage = toggleLanguage;
