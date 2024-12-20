CREATE TABLE Securities (
    `Securities_Code` VARCHAR(20) NOT NULL, -- Stock code, usually a string
    `sec_englishname` VARCHAR(100),         -- Company English name, string
    `ipo_date` DATE,                        -- IPO date, date type
    `exch_eng` VARCHAR(10),                 -- Exchange code, string
    `country` VARCHAR(10),                  -- Country code, string
    PRIMARY KEY (`Securities_Code`)         -- Primary key
);

CREATE TABLE Companies (
    `Company_code` VARCHAR(10) NOT NULL,       -- Company code, string, primary key
    `Securities_Code` VARCHAR(20),            -- Stock code, string
    `comp_name_eng` VARCHAR(255),             -- Company English name, string
    `phone` TEXT,                             -- Phone number(s), may contain multiple numbers, stored as TEXT
    `industry_swcode_2021` BIGINT,            -- Industry code, uses large integer type
    `founddate1` DATE,                        -- Establishment date, using DATE type
    `regcapital` DECIMAL(15, 4),              -- Registered capital, accurate to 4 decimal places
    `employee_number` INT,                    -- Number of employees, integer type
    PRIMARY KEY (`Company_code`),             -- Primary key
    FOREIGN KEY (`Securities_Code`) REFERENCES Securities(`Securities_Code`) -- Foreign key linking to Securities
);

CREATE TABLE balance_sheet (
    `balanceCode` VARCHAR(10) NOT NULL,              -- Balance sheet code
    `windcode` VARCHAR(20),                         -- Stock code
    `tot_assets` DECIMAL(15, 4),                    -- Total assets
    `tot_cur_assets` DECIMAL(15, 4),                -- Current assets
    `inventories` DECIMAL(15, 4),                   -- Inventories
    `fix_assets` DECIMAL(15, 4),                    -- Fixed assets
    `tot_liab` DECIMAL(15, 4),                      -- Total liabilities
    `tot_non_cur_liab` DECIMAL(15, 4),              -- Non-current liabilities
    `tot_cur_liab` DECIMAL(15, 4),                  -- Current liabilities
    `eqy_belongto_parcomsh` DECIMAL(15, 4),         -- Equity attributable to shareholders of the parent company
    PRIMARY KEY (`balanceCode`),                    -- Primary key
    FOREIGN KEY (`windcode`) REFERENCES Securities(`Securities_Code`) -- Foreign key linking to Securities
);

CREATE TABLE income_statement (
    `IncomeCode` VARCHAR(10) NOT NULL,              -- Income statement code
    `BalanceCode` VARCHAR(10) NOT NULL,             -- Balance sheet code
    `tot_oper_rev` DECIMAL(15, 4),                  -- Total operating revenue
    `tot_oper_cost` DECIMAL(15, 4),                 -- Total operating costs
    `opprofit` DECIMAL(15, 4),                      -- Operating profit
    `tot_profit` DECIMAL(15, 4),                    -- Total profit
    `tax` DECIMAL(15, 4),                           -- Taxes
    `net_profit_is` DECIMAL(15, 4),                 -- Net profit
    `tot_compreh_inc_parent_comp` DECIMAL(15, 4),   -- Comprehensive income attributable to the parent company
    `selling_dist_exp` DECIMAL(15, 4),              -- Selling expenses
    `gerl_admin_exp` DECIMAL(15, 4),                -- General and administrative expenses
    `rd_exp` DECIMAL(15, 4),                        -- R&D expenses
    `fin_exp_is` DECIMAL(15, 4),                    -- Financial expenses
    PRIMARY KEY (`IncomeCode`),                     -- Primary key
    FOREIGN KEY (`BalanceCode`) REFERENCES balance_sheet(`balanceCode`) -- Foreign key linking to balance_sheet
);

CREATE TABLE financial_analysis (
    `FAID` VARCHAR(10) NOT NULL,              -- Financial analysis table code
    `BalanceCode` VARCHAR(10) NOT NULL,       -- Balance sheet code
    `eps_basic` DECIMAL(15, 4),               -- Basic earnings per share
    `roe_basic` DECIMAL(15, 4),               -- Return on equity (basic)
    `profittogr` DECIMAL(15, 4),              -- Total profit growth rate
    `currentRatio` DECIMAL(15, 4),            -- Current ratio
    `quick` DECIMAL(15, 4),                   -- Quick ratio
    `fa_debttoeqy` DECIMAL(15, 4),            -- Financial leverage (debt-to-equity ratio)
    `invturndays` DECIMAL(15, 4),             -- Inventory turnover days
    `invturn` DECIMAL(15, 4),                 -- Inventory turnover rate
    `turnover_ttm` DECIMAL(15, 4),            -- Turnover (TTM)
    `yoy_tr` DECIMAL(15, 4),                  -- Year-over-year operating revenue growth rate
    `yoyprofit` DECIMAL(15, 4),               -- Year-over-year profit growth rate
    PRIMARY KEY (`FAID`),                     -- Primary key
    FOREIGN KEY (`BalanceCode`) REFERENCES balance_sheet(`balanceCode`) -- Foreign key linking to balance_sheet
);

CREATE TABLE esg_data (
    `ESG_reportID` VARCHAR(10) NOT NULL,          -- ESG report ID
    `Company_code` VARCHAR(10) NOT NULL,         -- Company code
    `esg_rating_wind` VARCHAR(10),               -- ESG rating (e.g., AA, BBB, etc.)
    `esg_escore_wind` DECIMAL(10, 2),            -- ESG environment score
    `esg_sscore_wind` DECIMAL(10, 2),            -- ESG social score
    `esg_gscore_wind` DECIMAL(10, 2),            -- ESG governance score
    `esg_rating_ftserussell` DECIMAL(10, 2),     -- FTSE Russell ESG rating (nullable)
    `esg_mgmtscore_wind2` DECIMAL(10, 3),        -- ESG management score
    `esg_eventscore_wind2` DECIMAL(10, 3),       -- ESG event score
    PRIMARY KEY (`ESG_reportID`),                -- Primary key
    FOREIGN KEY (`Company_code`) REFERENCES Companies(`Company_code`) -- Foreign key linking to Companies
);
