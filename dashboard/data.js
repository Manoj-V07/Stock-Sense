const STOCKSENSE_DATA = {
  "category_pareto": [
    {
      "category": "Beverages",
      "revenue": 8386009.5,
      "units_sold": 67559,
      "revenue_share": 0.1709059695618565,
      "cumulative_revenue_share": 0.1709059695618565
    },
    {
      "category": "Fruits & Vegetables",
      "revenue": 7862927.0,
      "units_sold": 27016,
      "revenue_share": 0.1602456046024155,
      "cumulative_revenue_share": 0.3311515741642721
    },
    {
      "category": "Snacks",
      "revenue": 7595693.5,
      "units_sold": 40184,
      "revenue_share": 0.1547994146813441,
      "cumulative_revenue_share": 0.4859509888456162
    },
    {
      "category": "Dairy",
      "revenue": 5566221.0,
      "units_sold": 26241,
      "revenue_share": 0.1134389839172692,
      "cumulative_revenue_share": 0.5993899727628855
    },
    {
      "category": "Personal Care",
      "revenue": 5016079.0,
      "units_sold": 31960,
      "revenue_share": 0.1022271492649594,
      "cumulative_revenue_share": 0.701617122027845
    },
    {
      "category": "Household",
      "revenue": 4725836.0,
      "units_sold": 35593,
      "revenue_share": 0.0963120282144118,
      "cumulative_revenue_share": 0.7979291502422569
    },
    {
      "category": "Frozen",
      "revenue": 3642216.0,
      "units_sold": 19594,
      "revenue_share": 0.0742279694333409,
      "cumulative_revenue_share": 0.8721571196755978
    },
    {
      "category": "Staples",
      "revenue": 3156969.0,
      "units_sold": 20785,
      "revenue_share": 0.0643386878850691,
      "cumulative_revenue_share": 0.936495807560667
    },
    {
      "category": "Bakery",
      "revenue": 3116022.0,
      "units_sold": 19829,
      "revenue_share": 0.063504192439333,
      "cumulative_revenue_share": 1.0
    }
  ],
  "store_performance": [
    {
      "store_id": "S01",
      "store_type": "Supermarket",
      "revenue": 4913967.0,
      "units_sold": 28570,
      "observations": 2927,
      "stockout_rate": 0.0004681647940074,
      "average_inventory": 433.2237827715356,
      "demand_volatility": 14.334026563810832
    },
    {
      "store_id": "S02",
      "store_type": "Hypermarket",
      "revenue": 5394211.5,
      "units_sold": 29512,
      "observations": 2909,
      "stockout_rate": 0.0014367816091954,
      "average_inventory": 440.2935823754789,
      "demand_volatility": 14.970153498691658
    },
    {
      "store_id": "S03",
      "store_type": "Express",
      "revenue": 4698522.5,
      "units_sold": 28280,
      "observations": 2888,
      "stockout_rate": 0.0038295835327908,
      "average_inventory": 427.60028721876495,
      "demand_volatility": 14.380274397327309
    },
    {
      "store_id": "S04",
      "store_type": "Supermarket",
      "revenue": 4867779.5,
      "units_sold": 28755,
      "observations": 2906,
      "stockout_rate": 0.0004728132387706,
      "average_inventory": 432.5588652482269,
      "demand_volatility": 14.586804550797364
    },
    {
      "store_id": "S05",
      "store_type": "Hypermarket",
      "revenue": 5044181.0,
      "units_sold": 29638,
      "observations": 2930,
      "stockout_rate": 0.0018788163457022,
      "average_inventory": 418.87036167214654,
      "demand_volatility": 14.685051483346196
    },
    {
      "store_id": "S06",
      "store_type": "Supermarket",
      "revenue": 4868869.5,
      "units_sold": 28946,
      "observations": 2870,
      "stockout_rate": 0.000966650555824,
      "average_inventory": 430.13533107781535,
      "demand_volatility": 14.802509776148003
    },
    {
      "store_id": "S07",
      "store_type": "Express",
      "revenue": 4705806.5,
      "units_sold": 28208,
      "observations": 2907,
      "stockout_rate": 0.0009638554216867,
      "average_inventory": 451.2853012048193,
      "demand_volatility": 14.534914119505627
    },
    {
      "store_id": "S08",
      "store_type": "Supermarket",
      "revenue": 4969171.0,
      "units_sold": 29348,
      "observations": 2929,
      "stockout_rate": 0.0014157621519584,
      "average_inventory": 428.5861255309108,
      "demand_volatility": 15.333060680247842
    },
    {
      "store_id": "S09",
      "store_type": "Hypermarket",
      "revenue": 4842162.0,
      "units_sold": 28889,
      "observations": 2917,
      "stockout_rate": 0.0014218009478672,
      "average_inventory": 433.714691943128,
      "demand_volatility": 14.735713952488506
    },
    {
      "store_id": "S10",
      "store_type": "Supermarket",
      "revenue": 4763302.5,
      "units_sold": 28615,
      "observations": 2896,
      "stockout_rate": 0.0024050024050024,
      "average_inventory": 426.86099086099085,
      "demand_volatility": 14.4485974746161
    }
  ],
  "kpis": [
    {
      "kpi": "Revenue",
      "value": 49067973.0,
      "definition": "Sum of aggregated transaction revenue"
    },
    {
      "kpi": "Units sold",
      "value": 288761.0,
      "definition": "Sum of transaction_demand"
    },
    {
      "kpi": "Stock-out rate",
      "value": 0.0015231567423485,
      "definition": "Observed closing <= 0 / rows with closing inventory"
    },
    {
      "kpi": "Inventory turnover",
      "value": 7683.457663387664,
      "definition": "COGS using inventory_sold x cost / mean closing inventory value; inventory rows only"
    },
    {
      "kpi": "Days of inventory",
      "value": 130.17397014251625,
      "definition": "Closing stock / same-row transaction demand; positive-demand rows only"
    },
    {
      "kpi": "Promotion lift",
      "value": 2.4261467362117943,
      "definition": "Mean row demand promoted vs normal minus 1; association, not causation"
    },
    {
      "kpi": "Estimated lost sales",
      "value": 39456.88102240896,
      "definition": "Observed stock-out rows x transaction demand x average selling price; descriptive proxy"
    }
  ],
  "agg_daily_trend": [
    {
      "date": "2026-07-31",
      "demand": 2,
      "revenue": 360.0,
      "stockouts": 0
    },
    {
      "date": "2026-08-01",
      "demand": 9133,
      "revenue": 1553871.5,
      "stockouts": 3
    },
    {
      "date": "2026-08-02",
      "demand": 9025,
      "revenue": 1549930.5,
      "stockouts": 0
    },
    {
      "date": "2026-08-03",
      "demand": 9146,
      "revenue": 1521088.5,
      "stockouts": 0
    },
    {
      "date": "2026-08-04",
      "demand": 9566,
      "revenue": 1609481.5,
      "stockouts": 1
    },
    {
      "date": "2026-08-05",
      "demand": 9461,
      "revenue": 1611993.5,
      "stockouts": 1
    },
    {
      "date": "2026-08-06",
      "demand": 9274,
      "revenue": 1544359.0,
      "stockouts": 0
    },
    {
      "date": "2026-08-07",
      "demand": 9488,
      "revenue": 1618396.5,
      "stockouts": 2
    },
    {
      "date": "2026-08-08",
      "demand": 9379,
      "revenue": 1940825.0,
      "stockouts": 0
    },
    {
      "date": "2026-08-09",
      "demand": 9344,
      "revenue": 1583396.0,
      "stockouts": 3
    },
    {
      "date": "2026-08-10",
      "demand": 9224,
      "revenue": 1564243.0,
      "stockouts": 0
    },
    {
      "date": "2026-08-11",
      "demand": 9496,
      "revenue": 1575286.0,
      "stockouts": 1
    },
    {
      "date": "2026-08-12",
      "demand": 8919,
      "revenue": 1519829.5,
      "stockouts": 2
    },
    {
      "date": "2026-08-13",
      "demand": 9189,
      "revenue": 1532083.0,
      "stockouts": 1
    },
    {
      "date": "2026-08-14",
      "demand": 9291,
      "revenue": 1623228.0,
      "stockouts": 3
    },
    {
      "date": "2026-08-15",
      "demand": 9286,
      "revenue": 1555202.0,
      "stockouts": 0
    },
    {
      "date": "2026-08-16",
      "demand": 9622,
      "revenue": 1645179.5,
      "stockouts": 2
    },
    {
      "date": "2026-08-17",
      "demand": 9134,
      "revenue": 1512754.0,
      "stockouts": 0
    },
    {
      "date": "2026-08-18",
      "demand": 8885,
      "revenue": 1496084.5,
      "stockouts": 0
    },
    {
      "date": "2026-08-19",
      "demand": 9889,
      "revenue": 1651570.0,
      "stockouts": 1
    },
    {
      "date": "2026-08-20",
      "demand": 9720,
      "revenue": 1615640.5,
      "stockouts": 1
    },
    {
      "date": "2026-08-21",
      "demand": 9163,
      "revenue": 1515005.0,
      "stockouts": 1
    },
    {
      "date": "2026-08-22",
      "demand": 9480,
      "revenue": 1592889.5,
      "stockouts": 3
    },
    {
      "date": "2026-08-23",
      "demand": 9413,
      "revenue": 1618557.0,
      "stockouts": 0
    },
    {
      "date": "2026-08-24",
      "demand": 9304,
      "revenue": 1550360.0,
      "stockouts": 1
    },
    {
      "date": "2026-08-25",
      "demand": 8909,
      "revenue": 1490444.5,
      "stockouts": 1
    },
    {
      "date": "2026-08-26",
      "demand": 9430,
      "revenue": 1631227.5,
      "stockouts": 0
    },
    {
      "date": "2026-08-27",
      "demand": 8961,
      "revenue": 1505480.5,
      "stockouts": 1
    },
    {
      "date": "2026-08-28",
      "demand": 9226,
      "revenue": 1522319.0,
      "stockouts": 0
    },
    {
      "date": "2026-08-29",
      "demand": 9502,
      "revenue": 1646911.0,
      "stockouts": 1
    },
    {
      "date": "2026-08-30",
      "demand": 9627,
      "revenue": 1626607.0,
      "stockouts": 3
    },
    {
      "date": "2026-08-31",
      "demand": 9272,
      "revenue": 1543327.5,
      "stockouts": 0
    },
    {
      "date": "2026-09-01",
      "demand": 1,
      "revenue": 42.5,
      "stockouts": 0
    }
  ],
  "store_daily": {
    "S01": [
      {
        "date": "2026-08-01",
        "demand": 824,
        "revenue": 143937.0
      },
      {
        "date": "2026-08-02",
        "demand": 888,
        "revenue": 160594.0
      },
      {
        "date": "2026-08-03",
        "demand": 880,
        "revenue": 143005.5
      },
      {
        "date": "2026-08-04",
        "demand": 1057,
        "revenue": 181943.5
      },
      {
        "date": "2026-08-05",
        "demand": 926,
        "revenue": 179126.5
      },
      {
        "date": "2026-08-06",
        "demand": 912,
        "revenue": 143277.5
      },
      {
        "date": "2026-08-07",
        "demand": 935,
        "revenue": 161458.5
      },
      {
        "date": "2026-08-08",
        "demand": 951,
        "revenue": 170559.5
      },
      {
        "date": "2026-08-09",
        "demand": 867,
        "revenue": 150847.5
      },
      {
        "date": "2026-08-10",
        "demand": 885,
        "revenue": 148196.0
      },
      {
        "date": "2026-08-11",
        "demand": 816,
        "revenue": 121730.0
      },
      {
        "date": "2026-08-12",
        "demand": 859,
        "revenue": 143594.5
      },
      {
        "date": "2026-08-13",
        "demand": 1007,
        "revenue": 173254.5
      },
      {
        "date": "2026-08-14",
        "demand": 1076,
        "revenue": 206650.0
      },
      {
        "date": "2026-08-15",
        "demand": 1058,
        "revenue": 191052.5
      },
      {
        "date": "2026-08-16",
        "demand": 874,
        "revenue": 148220.5
      },
      {
        "date": "2026-08-17",
        "demand": 850,
        "revenue": 155542.5
      },
      {
        "date": "2026-08-18",
        "demand": 899,
        "revenue": 148325.5
      },
      {
        "date": "2026-08-19",
        "demand": 902,
        "revenue": 157678.0
      },
      {
        "date": "2026-08-20",
        "demand": 961,
        "revenue": 165253.0
      },
      {
        "date": "2026-08-21",
        "demand": 883,
        "revenue": 157343.0
      },
      {
        "date": "2026-08-22",
        "demand": 1010,
        "revenue": 179822.5
      },
      {
        "date": "2026-08-23",
        "demand": 991,
        "revenue": 166397.5
      },
      {
        "date": "2026-08-24",
        "demand": 935,
        "revenue": 168029.0
      },
      {
        "date": "2026-08-25",
        "demand": 813,
        "revenue": 142015.0
      },
      {
        "date": "2026-08-26",
        "demand": 952,
        "revenue": 167401.5
      },
      {
        "date": "2026-08-27",
        "demand": 858,
        "revenue": 142733.0
      },
      {
        "date": "2026-08-28",
        "demand": 849,
        "revenue": 130310.0
      },
      {
        "date": "2026-08-29",
        "demand": 933,
        "revenue": 162397.0
      },
      {
        "date": "2026-08-30",
        "demand": 881,
        "revenue": 150108.0
      },
      {
        "date": "2026-08-31",
        "demand": 1038,
        "revenue": 153164.0
      }
    ],
    "S02": [
      {
        "date": "2026-08-01",
        "demand": 1038,
        "revenue": 175987.0
      },
      {
        "date": "2026-08-02",
        "demand": 913,
        "revenue": 142347.5
      },
      {
        "date": "2026-08-03",
        "demand": 877,
        "revenue": 141622.5
      },
      {
        "date": "2026-08-04",
        "demand": 881,
        "revenue": 140578.0
      },
      {
        "date": "2026-08-05",
        "demand": 850,
        "revenue": 149395.0
      },
      {
        "date": "2026-08-06",
        "demand": 887,
        "revenue": 148391.0
      },
      {
        "date": "2026-08-07",
        "demand": 926,
        "revenue": 147055.5
      },
      {
        "date": "2026-08-08",
        "demand": 1005,
        "revenue": 555709.0
      },
      {
        "date": "2026-08-09",
        "demand": 916,
        "revenue": 174458.5
      },
      {
        "date": "2026-08-10",
        "demand": 1041,
        "revenue": 187382.5
      },
      {
        "date": "2026-08-11",
        "demand": 956,
        "revenue": 156457.5
      },
      {
        "date": "2026-08-12",
        "demand": 962,
        "revenue": 164439.5
      },
      {
        "date": "2026-08-13",
        "demand": 1010,
        "revenue": 174261.5
      },
      {
        "date": "2026-08-14",
        "demand": 1007,
        "revenue": 165911.0
      },
      {
        "date": "2026-08-15",
        "demand": 1038,
        "revenue": 194934.0
      },
      {
        "date": "2026-08-16",
        "demand": 951,
        "revenue": 163078.0
      },
      {
        "date": "2026-08-17",
        "demand": 1005,
        "revenue": 172944.0
      },
      {
        "date": "2026-08-18",
        "demand": 825,
        "revenue": 133280.0
      },
      {
        "date": "2026-08-19",
        "demand": 999,
        "revenue": 160732.0
      },
      {
        "date": "2026-08-20",
        "demand": 1081,
        "revenue": 178134.5
      },
      {
        "date": "2026-08-21",
        "demand": 898,
        "revenue": 148409.5
      },
      {
        "date": "2026-08-22",
        "demand": 870,
        "revenue": 136609.0
      },
      {
        "date": "2026-08-23",
        "demand": 973,
        "revenue": 167184.0
      },
      {
        "date": "2026-08-24",
        "demand": 928,
        "revenue": 159273.0
      },
      {
        "date": "2026-08-25",
        "demand": 883,
        "revenue": 149867.5
      },
      {
        "date": "2026-08-26",
        "demand": 863,
        "revenue": 152861.5
      },
      {
        "date": "2026-08-27",
        "demand": 954,
        "revenue": 175906.5
      },
      {
        "date": "2026-08-28",
        "demand": 996,
        "revenue": 175080.0
      },
      {
        "date": "2026-08-29",
        "demand": 1042,
        "revenue": 170375.0
      },
      {
        "date": "2026-08-30",
        "demand": 1020,
        "revenue": 169276.0
      },
      {
        "date": "2026-08-31",
        "demand": 917,
        "revenue": 162271.0
      }
    ],
    "S03": [
      {
        "date": "2026-07-31",
        "demand": 2,
        "revenue": 360.0
      },
      {
        "date": "2026-08-01",
        "demand": 858,
        "revenue": 146996.0
      },
      {
        "date": "2026-08-02",
        "demand": 905,
        "revenue": 146488.5
      },
      {
        "date": "2026-08-03",
        "demand": 983,
        "revenue": 167871.5
      },
      {
        "date": "2026-08-04",
        "demand": 794,
        "revenue": 138901.5
      },
      {
        "date": "2026-08-05",
        "demand": 987,
        "revenue": 167318.5
      },
      {
        "date": "2026-08-06",
        "demand": 926,
        "revenue": 152480.0
      },
      {
        "date": "2026-08-07",
        "demand": 792,
        "revenue": 134575.0
      },
      {
        "date": "2026-08-08",
        "demand": 902,
        "revenue": 144694.5
      },
      {
        "date": "2026-08-09",
        "demand": 882,
        "revenue": 152019.0
      },
      {
        "date": "2026-08-10",
        "demand": 1000,
        "revenue": 169865.5
      },
      {
        "date": "2026-08-11",
        "demand": 825,
        "revenue": 123968.5
      },
      {
        "date": "2026-08-12",
        "demand": 950,
        "revenue": 168507.0
      },
      {
        "date": "2026-08-13",
        "demand": 784,
        "revenue": 131776.0
      },
      {
        "date": "2026-08-14",
        "demand": 823,
        "revenue": 143075.0
      },
      {
        "date": "2026-08-15",
        "demand": 770,
        "revenue": 126486.5
      },
      {
        "date": "2026-08-16",
        "demand": 1005,
        "revenue": 174630.0
      },
      {
        "date": "2026-08-17",
        "demand": 1033,
        "revenue": 163462.0
      },
      {
        "date": "2026-08-18",
        "demand": 781,
        "revenue": 141431.5
      },
      {
        "date": "2026-08-19",
        "demand": 1024,
        "revenue": 167595.0
      },
      {
        "date": "2026-08-20",
        "demand": 966,
        "revenue": 162938.0
      },
      {
        "date": "2026-08-21",
        "demand": 823,
        "revenue": 129800.0
      },
      {
        "date": "2026-08-22",
        "demand": 922,
        "revenue": 150280.0
      },
      {
        "date": "2026-08-23",
        "demand": 887,
        "revenue": 160505.0
      },
      {
        "date": "2026-08-24",
        "demand": 1007,
        "revenue": 165367.0
      },
      {
        "date": "2026-08-25",
        "demand": 983,
        "revenue": 148343.5
      },
      {
        "date": "2026-08-26",
        "demand": 979,
        "revenue": 155722.0
      },
      {
        "date": "2026-08-27",
        "demand": 853,
        "revenue": 148647.5
      },
      {
        "date": "2026-08-28",
        "demand": 918,
        "revenue": 146822.5
      },
      {
        "date": "2026-08-29",
        "demand": 973,
        "revenue": 150108.0
      },
      {
        "date": "2026-08-30",
        "demand": 1062,
        "revenue": 175250.5
      },
      {
        "date": "2026-08-31",
        "demand": 880,
        "revenue": 142194.5
      },
      {
        "date": "2026-09-01",
        "demand": 1,
        "revenue": 42.5
      }
    ],
    "S04": [
      {
        "date": "2026-08-01",
        "demand": 988,
        "revenue": 168093.0
      },
      {
        "date": "2026-08-02",
        "demand": 857,
        "revenue": 147304.0
      },
      {
        "date": "2026-08-03",
        "demand": 861,
        "revenue": 143688.5
      },
      {
        "date": "2026-08-04",
        "demand": 964,
        "revenue": 165269.5
      },
      {
        "date": "2026-08-05",
        "demand": 1007,
        "revenue": 164057.5
      },
      {
        "date": "2026-08-06",
        "demand": 865,
        "revenue": 156183.5
      },
      {
        "date": "2026-08-07",
        "demand": 788,
        "revenue": 139079.0
      },
      {
        "date": "2026-08-08",
        "demand": 873,
        "revenue": 127454.5
      },
      {
        "date": "2026-08-09",
        "demand": 1044,
        "revenue": 161535.5
      },
      {
        "date": "2026-08-10",
        "demand": 933,
        "revenue": 150403.0
      },
      {
        "date": "2026-08-11",
        "demand": 983,
        "revenue": 170029.5
      },
      {
        "date": "2026-08-12",
        "demand": 891,
        "revenue": 157177.5
      },
      {
        "date": "2026-08-13",
        "demand": 1085,
        "revenue": 175178.5
      },
      {
        "date": "2026-08-14",
        "demand": 954,
        "revenue": 167913.5
      },
      {
        "date": "2026-08-15",
        "demand": 886,
        "revenue": 151390.0
      },
      {
        "date": "2026-08-16",
        "demand": 932,
        "revenue": 164167.5
      },
      {
        "date": "2026-08-17",
        "demand": 818,
        "revenue": 131872.0
      },
      {
        "date": "2026-08-18",
        "demand": 950,
        "revenue": 160265.5
      },
      {
        "date": "2026-08-19",
        "demand": 983,
        "revenue": 178506.0
      },
      {
        "date": "2026-08-20",
        "demand": 1018,
        "revenue": 161493.5
      },
      {
        "date": "2026-08-21",
        "demand": 822,
        "revenue": 124670.5
      },
      {
        "date": "2026-08-22",
        "demand": 1080,
        "revenue": 194614.5
      },
      {
        "date": "2026-08-23",
        "demand": 956,
        "revenue": 174267.0
      },
      {
        "date": "2026-08-24",
        "demand": 968,
        "revenue": 157913.0
      },
      {
        "date": "2026-08-25",
        "demand": 858,
        "revenue": 148472.0
      },
      {
        "date": "2026-08-26",
        "demand": 827,
        "revenue": 132295.5
      },
      {
        "date": "2026-08-27",
        "demand": 975,
        "revenue": 169592.5
      },
      {
        "date": "2026-08-28",
        "demand": 812,
        "revenue": 126137.0
      },
      {
        "date": "2026-08-29",
        "demand": 828,
        "revenue": 143371.0
      },
      {
        "date": "2026-08-30",
        "demand": 1095,
        "revenue": 214391.5
      },
      {
        "date": "2026-08-31",
        "demand": 854,
        "revenue": 140993.5
      }
    ],
    "S05": [
      {
        "date": "2026-08-01",
        "demand": 955,
        "revenue": 171162.0
      },
      {
        "date": "2026-08-02",
        "demand": 1068,
        "revenue": 196687.5
      },
      {
        "date": "2026-08-03",
        "demand": 881,
        "revenue": 148420.0
      },
      {
        "date": "2026-08-04",
        "demand": 1009,
        "revenue": 170672.0
      },
      {
        "date": "2026-08-05",
        "demand": 1075,
        "revenue": 181766.0
      },
      {
        "date": "2026-08-06",
        "demand": 986,
        "revenue": 155315.0
      },
      {
        "date": "2026-08-07",
        "demand": 1014,
        "revenue": 172941.5
      },
      {
        "date": "2026-08-08",
        "demand": 977,
        "revenue": 170518.0
      },
      {
        "date": "2026-08-09",
        "demand": 1025,
        "revenue": 162347.0
      },
      {
        "date": "2026-08-10",
        "demand": 848,
        "revenue": 142329.0
      },
      {
        "date": "2026-08-11",
        "demand": 1047,
        "revenue": 178882.5
      },
      {
        "date": "2026-08-12",
        "demand": 838,
        "revenue": 148704.5
      },
      {
        "date": "2026-08-13",
        "demand": 925,
        "revenue": 141595.5
      },
      {
        "date": "2026-08-14",
        "demand": 940,
        "revenue": 160776.0
      },
      {
        "date": "2026-08-15",
        "demand": 932,
        "revenue": 156220.5
      },
      {
        "date": "2026-08-16",
        "demand": 1093,
        "revenue": 186681.5
      },
      {
        "date": "2026-08-17",
        "demand": 989,
        "revenue": 173008.5
      },
      {
        "date": "2026-08-18",
        "demand": 827,
        "revenue": 139800.0
      },
      {
        "date": "2026-08-19",
        "demand": 1050,
        "revenue": 176354.5
      },
      {
        "date": "2026-08-20",
        "demand": 1081,
        "revenue": 197824.5
      },
      {
        "date": "2026-08-21",
        "demand": 835,
        "revenue": 141597.0
      },
      {
        "date": "2026-08-22",
        "demand": 869,
        "revenue": 156786.5
      },
      {
        "date": "2026-08-23",
        "demand": 1007,
        "revenue": 177797.0
      },
      {
        "date": "2026-08-24",
        "demand": 867,
        "revenue": 139262.5
      },
      {
        "date": "2026-08-25",
        "demand": 872,
        "revenue": 135907.0
      },
      {
        "date": "2026-08-26",
        "demand": 829,
        "revenue": 152712.5
      },
      {
        "date": "2026-08-27",
        "demand": 835,
        "revenue": 131276.5
      },
      {
        "date": "2026-08-28",
        "demand": 1006,
        "revenue": 167890.5
      },
      {
        "date": "2026-08-29",
        "demand": 1048,
        "revenue": 191662.5
      },
      {
        "date": "2026-08-30",
        "demand": 915,
        "revenue": 145554.5
      },
      {
        "date": "2026-08-31",
        "demand": 995,
        "revenue": 171728.5
      }
    ],
    "S06": [
      {
        "date": "2026-08-01",
        "demand": 971,
        "revenue": 159596.0
      },
      {
        "date": "2026-08-02",
        "demand": 813,
        "revenue": 150610.0
      },
      {
        "date": "2026-08-03",
        "demand": 806,
        "revenue": 143929.5
      },
      {
        "date": "2026-08-04",
        "demand": 994,
        "revenue": 162966.5
      },
      {
        "date": "2026-08-05",
        "demand": 985,
        "revenue": 155974.5
      },
      {
        "date": "2026-08-06",
        "demand": 878,
        "revenue": 170625.5
      },
      {
        "date": "2026-08-07",
        "demand": 929,
        "revenue": 154726.0
      },
      {
        "date": "2026-08-08",
        "demand": 897,
        "revenue": 164614.0
      },
      {
        "date": "2026-08-09",
        "demand": 918,
        "revenue": 158980.5
      },
      {
        "date": "2026-08-10",
        "demand": 817,
        "revenue": 135933.0
      },
      {
        "date": "2026-08-11",
        "demand": 1007,
        "revenue": 163299.0
      },
      {
        "date": "2026-08-12",
        "demand": 821,
        "revenue": 137773.0
      },
      {
        "date": "2026-08-13",
        "demand": 808,
        "revenue": 142764.0
      },
      {
        "date": "2026-08-14",
        "demand": 846,
        "revenue": 140624.5
      },
      {
        "date": "2026-08-15",
        "demand": 1016,
        "revenue": 169693.5
      },
      {
        "date": "2026-08-16",
        "demand": 1007,
        "revenue": 159849.5
      },
      {
        "date": "2026-08-17",
        "demand": 1078,
        "revenue": 181419.0
      },
      {
        "date": "2026-08-18",
        "demand": 1003,
        "revenue": 177441.0
      },
      {
        "date": "2026-08-19",
        "demand": 921,
        "revenue": 147625.5
      },
      {
        "date": "2026-08-20",
        "demand": 856,
        "revenue": 131080.5
      },
      {
        "date": "2026-08-21",
        "demand": 1005,
        "revenue": 172047.5
      },
      {
        "date": "2026-08-22",
        "demand": 949,
        "revenue": 161991.5
      },
      {
        "date": "2026-08-23",
        "demand": 1020,
        "revenue": 163983.0
      },
      {
        "date": "2026-08-24",
        "demand": 950,
        "revenue": 141846.0
      },
      {
        "date": "2026-08-25",
        "demand": 907,
        "revenue": 169439.0
      },
      {
        "date": "2026-08-26",
        "demand": 867,
        "revenue": 147929.5
      },
      {
        "date": "2026-08-27",
        "demand": 865,
        "revenue": 135940.0
      },
      {
        "date": "2026-08-28",
        "demand": 1097,
        "revenue": 186958.0
      },
      {
        "date": "2026-08-29",
        "demand": 967,
        "revenue": 155163.5
      },
      {
        "date": "2026-08-30",
        "demand": 1029,
        "revenue": 171982.0
      },
      {
        "date": "2026-08-31",
        "demand": 919,
        "revenue": 152064.5
      }
    ],
    "S07": [
      {
        "date": "2026-08-01",
        "demand": 827,
        "revenue": 139790.0
      },
      {
        "date": "2026-08-02",
        "demand": 880,
        "revenue": 149655.0
      },
      {
        "date": "2026-08-03",
        "demand": 798,
        "revenue": 131922.0
      },
      {
        "date": "2026-08-04",
        "demand": 1023,
        "revenue": 174930.5
      },
      {
        "date": "2026-08-05",
        "demand": 824,
        "revenue": 139356.0
      },
      {
        "date": "2026-08-06",
        "demand": 1082,
        "revenue": 191427.0
      },
      {
        "date": "2026-08-07",
        "demand": 1021,
        "revenue": 193452.5
      },
      {
        "date": "2026-08-08",
        "demand": 1071,
        "revenue": 173001.0
      },
      {
        "date": "2026-08-09",
        "demand": 789,
        "revenue": 120239.0
      },
      {
        "date": "2026-08-10",
        "demand": 887,
        "revenue": 149851.5
      },
      {
        "date": "2026-08-11",
        "demand": 1011,
        "revenue": 166517.0
      },
      {
        "date": "2026-08-12",
        "demand": 857,
        "revenue": 139062.5
      },
      {
        "date": "2026-08-13",
        "demand": 878,
        "revenue": 152443.5
      },
      {
        "date": "2026-08-14",
        "demand": 779,
        "revenue": 130163.5
      },
      {
        "date": "2026-08-15",
        "demand": 850,
        "revenue": 134574.5
      },
      {
        "date": "2026-08-16",
        "demand": 994,
        "revenue": 162730.5
      },
      {
        "date": "2026-08-17",
        "demand": 934,
        "revenue": 153919.0
      },
      {
        "date": "2026-08-18",
        "demand": 830,
        "revenue": 128298.5
      },
      {
        "date": "2026-08-19",
        "demand": 1025,
        "revenue": 157581.0
      },
      {
        "date": "2026-08-20",
        "demand": 845,
        "revenue": 142280.0
      },
      {
        "date": "2026-08-21",
        "demand": 1025,
        "revenue": 166111.5
      },
      {
        "date": "2026-08-22",
        "demand": 844,
        "revenue": 140318.5
      },
      {
        "date": "2026-08-23",
        "demand": 916,
        "revenue": 149587.5
      },
      {
        "date": "2026-08-24",
        "demand": 925,
        "revenue": 149789.5
      },
      {
        "date": "2026-08-25",
        "demand": 864,
        "revenue": 143292.5
      },
      {
        "date": "2026-08-26",
        "demand": 1045,
        "revenue": 183389.0
      },
      {
        "date": "2026-08-27",
        "demand": 998,
        "revenue": 164684.0
      },
      {
        "date": "2026-08-28",
        "demand": 838,
        "revenue": 144816.5
      },
      {
        "date": "2026-08-29",
        "demand": 817,
        "revenue": 138041.0
      },
      {
        "date": "2026-08-30",
        "demand": 815,
        "revenue": 134527.0
      },
      {
        "date": "2026-08-31",
        "demand": 916,
        "revenue": 160055.0
      }
    ],
    "S08": [
      {
        "date": "2026-08-01",
        "demand": 803,
        "revenue": 139089.0
      },
      {
        "date": "2026-08-02",
        "demand": 826,
        "revenue": 133582.0
      },
      {
        "date": "2026-08-03",
        "demand": 1062,
        "revenue": 156422.0
      },
      {
        "date": "2026-08-04",
        "demand": 950,
        "revenue": 166035.0
      },
      {
        "date": "2026-08-05",
        "demand": 934,
        "revenue": 170914.0
      },
      {
        "date": "2026-08-06",
        "demand": 873,
        "revenue": 141184.5
      },
      {
        "date": "2026-08-07",
        "demand": 1023,
        "revenue": 177493.5
      },
      {
        "date": "2026-08-08",
        "demand": 807,
        "revenue": 121896.5
      },
      {
        "date": "2026-08-09",
        "demand": 1042,
        "revenue": 192990.5
      },
      {
        "date": "2026-08-10",
        "demand": 1004,
        "revenue": 179070.0
      },
      {
        "date": "2026-08-11",
        "demand": 1027,
        "revenue": 180320.5
      },
      {
        "date": "2026-08-12",
        "demand": 947,
        "revenue": 159909.5
      },
      {
        "date": "2026-08-13",
        "demand": 869,
        "revenue": 150974.5
      },
      {
        "date": "2026-08-14",
        "demand": 1051,
        "revenue": 189977.0
      },
      {
        "date": "2026-08-15",
        "demand": 970,
        "revenue": 152248.0
      },
      {
        "date": "2026-08-16",
        "demand": 1119,
        "revenue": 186317.5
      },
      {
        "date": "2026-08-17",
        "demand": 785,
        "revenue": 120349.5
      },
      {
        "date": "2026-08-18",
        "demand": 914,
        "revenue": 159372.5
      },
      {
        "date": "2026-08-19",
        "demand": 1041,
        "revenue": 181024.0
      },
      {
        "date": "2026-08-20",
        "demand": 887,
        "revenue": 142669.0
      },
      {
        "date": "2026-08-21",
        "demand": 974,
        "revenue": 162703.0
      },
      {
        "date": "2026-08-22",
        "demand": 849,
        "revenue": 137175.5
      },
      {
        "date": "2026-08-23",
        "demand": 918,
        "revenue": 153411.5
      },
      {
        "date": "2026-08-24",
        "demand": 946,
        "revenue": 159153.0
      },
      {
        "date": "2026-08-25",
        "demand": 1038,
        "revenue": 172985.5
      },
      {
        "date": "2026-08-26",
        "demand": 1007,
        "revenue": 175952.0
      },
      {
        "date": "2026-08-27",
        "demand": 885,
        "revenue": 143217.5
      },
      {
        "date": "2026-08-28",
        "demand": 944,
        "revenue": 157020.0
      },
      {
        "date": "2026-08-29",
        "demand": 863,
        "revenue": 170157.0
      },
      {
        "date": "2026-08-30",
        "demand": 948,
        "revenue": 164183.0
      },
      {
        "date": "2026-08-31",
        "demand": 1042,
        "revenue": 171374.0
      }
    ],
    "S09": [
      {
        "date": "2026-08-01",
        "demand": 986,
        "revenue": 169569.5
      },
      {
        "date": "2026-08-02",
        "demand": 989,
        "revenue": 164937.0
      },
      {
        "date": "2026-08-03",
        "demand": 920,
        "revenue": 160818.5
      },
      {
        "date": "2026-08-04",
        "demand": 941,
        "revenue": 148523.5
      },
      {
        "date": "2026-08-05",
        "demand": 893,
        "revenue": 146406.5
      },
      {
        "date": "2026-08-06",
        "demand": 837,
        "revenue": 135082.0
      },
      {
        "date": "2026-08-07",
        "demand": 1114,
        "revenue": 183690.0
      },
      {
        "date": "2026-08-08",
        "demand": 988,
        "revenue": 150505.0
      },
      {
        "date": "2026-08-09",
        "demand": 876,
        "revenue": 148006.0
      },
      {
        "date": "2026-08-10",
        "demand": 972,
        "revenue": 173745.5
      },
      {
        "date": "2026-08-11",
        "demand": 971,
        "revenue": 164186.0
      },
      {
        "date": "2026-08-12",
        "demand": 883,
        "revenue": 146817.0
      },
      {
        "date": "2026-08-13",
        "demand": 974,
        "revenue": 154532.5
      },
      {
        "date": "2026-08-14",
        "demand": 855,
        "revenue": 144394.5
      },
      {
        "date": "2026-08-15",
        "demand": 885,
        "revenue": 142057.0
      },
      {
        "date": "2026-08-16",
        "demand": 836,
        "revenue": 155923.5
      },
      {
        "date": "2026-08-17",
        "demand": 861,
        "revenue": 135062.0
      },
      {
        "date": "2026-08-18",
        "demand": 1059,
        "revenue": 171996.5
      },
      {
        "date": "2026-08-19",
        "demand": 964,
        "revenue": 163650.5
      },
      {
        "date": "2026-08-20",
        "demand": 1044,
        "revenue": 168611.5
      },
      {
        "date": "2026-08-21",
        "demand": 952,
        "revenue": 153854.0
      },
      {
        "date": "2026-08-22",
        "demand": 1057,
        "revenue": 169473.0
      },
      {
        "date": "2026-08-23",
        "demand": 790,
        "revenue": 140133.0
      },
      {
        "date": "2026-08-24",
        "demand": 808,
        "revenue": 152185.0
      },
      {
        "date": "2026-08-25",
        "demand": 805,
        "revenue": 140624.0
      },
      {
        "date": "2026-08-26",
        "demand": 1032,
        "revenue": 168427.5
      },
      {
        "date": "2026-08-27",
        "demand": 883,
        "revenue": 158071.5
      },
      {
        "date": "2026-08-28",
        "demand": 870,
        "revenue": 136832.5
      },
      {
        "date": "2026-08-29",
        "demand": 1069,
        "revenue": 195313.5
      },
      {
        "date": "2026-08-30",
        "demand": 941,
        "revenue": 155592.0
      },
      {
        "date": "2026-08-31",
        "demand": 834,
        "revenue": 143141.5
      }
    ],
    "S10": [
      {
        "date": "2026-08-01",
        "demand": 883,
        "revenue": 139652.0
      },
      {
        "date": "2026-08-02",
        "demand": 886,
        "revenue": 157725.0
      },
      {
        "date": "2026-08-03",
        "demand": 1078,
        "revenue": 183388.5
      },
      {
        "date": "2026-08-04",
        "demand": 953,
        "revenue": 159661.5
      },
      {
        "date": "2026-08-05",
        "demand": 980,
        "revenue": 157679.0
      },
      {
        "date": "2026-08-06",
        "demand": 1028,
        "revenue": 150393.0
      },
      {
        "date": "2026-08-07",
        "demand": 946,
        "revenue": 153925.0
      },
      {
        "date": "2026-08-08",
        "demand": 908,
        "revenue": 161873.0
      },
      {
        "date": "2026-08-09",
        "demand": 985,
        "revenue": 161972.5
      },
      {
        "date": "2026-08-10",
        "demand": 837,
        "revenue": 127467.0
      },
      {
        "date": "2026-08-11",
        "demand": 853,
        "revenue": 149895.5
      },
      {
        "date": "2026-08-12",
        "demand": 911,
        "revenue": 153844.5
      },
      {
        "date": "2026-08-13",
        "demand": 849,
        "revenue": 135302.5
      },
      {
        "date": "2026-08-14",
        "demand": 960,
        "revenue": 173743.0
      },
      {
        "date": "2026-08-15",
        "demand": 881,
        "revenue": 136545.5
      },
      {
        "date": "2026-08-16",
        "demand": 811,
        "revenue": 143581.0
      },
      {
        "date": "2026-08-17",
        "demand": 781,
        "revenue": 125175.5
      },
      {
        "date": "2026-08-18",
        "demand": 797,
        "revenue": 135873.5
      },
      {
        "date": "2026-08-19",
        "demand": 980,
        "revenue": 160823.5
      },
      {
        "date": "2026-08-20",
        "demand": 981,
        "revenue": 165356.0
      },
      {
        "date": "2026-08-21",
        "demand": 946,
        "revenue": 158469.0
      },
      {
        "date": "2026-08-22",
        "demand": 1030,
        "revenue": 165818.5
      },
      {
        "date": "2026-08-23",
        "demand": 955,
        "revenue": 165291.5
      },
      {
        "date": "2026-08-24",
        "demand": 970,
        "revenue": 157542.0
      },
      {
        "date": "2026-08-25",
        "demand": 886,
        "revenue": 139498.5
      },
      {
        "date": "2026-08-26",
        "demand": 1029,
        "revenue": 194536.5
      },
      {
        "date": "2026-08-27",
        "demand": 855,
        "revenue": 135411.5
      },
      {
        "date": "2026-08-28",
        "demand": 896,
        "revenue": 150452.0
      },
      {
        "date": "2026-08-29",
        "demand": 962,
        "revenue": 170322.5
      },
      {
        "date": "2026-08-30",
        "demand": 921,
        "revenue": 145742.5
      },
      {
        "date": "2026-08-31",
        "demand": 877,
        "revenue": 146341.0
      }
    ]
  },
  "promotion_lift": [
    {
      "category": "Bakery",
      "normal_mean_demand": 4.262218045112782,
      "promoted_mean_demand": 9.130746268656717,
      "promotion_lift": 1.1422522667807602
    },
    {
      "category": "Beverages",
      "normal_mean_demand": 4.287965616045845,
      "promoted_mean_demand": 23.061048689138577,
      "promotion_lift": 4.378086196130547
    },
    {
      "category": "Dairy",
      "normal_mean_demand": 3.449307075127644,
      "promoted_mean_demand": 11.8003291278113,
      "promotion_lift": 2.421072369259736
    },
    {
      "category": "Frozen",
      "normal_mean_demand": 4.055879899916597,
      "promoted_mean_demand": 7.979956663055255,
      "promotion_lift": 0.9675031953533312
    },
    {
      "category": "Fruits & Vegetables",
      "normal_mean_demand": 3.6161048689138577,
      "promoted_mean_demand": 12.856191004997225,
      "promotion_lift": 2.555259449336363
    },
    {
      "category": "Household",
      "normal_mean_demand": 4.307881773399015,
      "promoted_mean_demand": 12.070803500397773,
      "promotion_lift": 1.802027570704114
    },
    {
      "category": "Personal Care",
      "normal_mean_demand": 3.96144578313253,
      "promoted_mean_demand": 12.77919621749409,
      "promotion_lift": 2.2258919892092743
    },
    {
      "category": "Snacks",
      "normal_mean_demand": 4.057287278854254,
      "promoted_mean_demand": 16.149771689497715,
      "promotion_lift": 2.9804358379222986
    },
    {
      "category": "Staples",
      "normal_mean_demand": 3.530821917808219,
      "promoted_mean_demand": 10.896664486592543,
      "promotion_lift": 2.08615521831719
    }
  ],
  "statistical_tests": [
    {
      "business_question": "Promotion and demand",
      "test": "Mann-Whitney U",
      "statistic": 156705659.0,
      "p_value": 0.0,
      "decision": "Reject"
    },
    {
      "business_question": "Mean demand across store types",
      "test": "Kruskal-Wallis",
      "statistic": 2.610209788055781,
      "p_value": 0.2711440921579163,
      "decision": "Do not reject"
    },
    {
      "business_question": "Promotion status and stock-out frequency",
      "test": "Chi-square independence",
      "statistic": 0.9849007346343162,
      "p_value": 0.3209918813274184,
      "decision": "Do not reject"
    }
  ],
  "demand_model_comparison": [
    {
      "model": "RandomForestRegressor",
      "val_mae": 9.674458360832784,
      "val_r2": 0.9794850428059644,
      "test_mae": 11.71862776304156,
      "test_r2": 0.9648521186614614
    },
    {
      "model": "XGBRegressor",
      "val_mae": 10.00458557344269,
      "val_r2": 0.9773468664635916,
      "test_mae": 11.477427950319624,
      "test_r2": 0.9667326038855024
    },
    {
      "model": "DecisionTreeRegressor",
      "val_mae": 11.099198996995831,
      "val_r2": 0.970171945979182,
      "test_mae": 13.037420728427424,
      "test_r2": 0.9520919664364594
    },
    {
      "model": "KNeighborsRegressor",
      "val_mae": 20.388933221335574,
      "val_r2": 0.9343219349809228,
      "test_mae": 22.25718832891247,
      "test_r2": 0.92004584300512
    },
    {
      "model": "SVR",
      "val_mae": 61.02384868263779,
      "val_r2": -0.0147764431990624,
      "test_mae": 61.91890328151753,
      "test_r2": -0.0347134639129251
    },
    {
      "model": "LinearRegression",
      "val_mae": 84.28612110867175,
      "val_r2": -1.2628981211269965,
      "test_mae": 84.68159639410172,
      "test_r2": -1.4086084360047026
    }
  ],
  "stockout_model_comparison": [
    {
      "model": "DecisionTreeClassifier",
      "val_f1": 1.0,
      "val_roc_auc": 1.0,
      "test_f1": 1.0,
      "test_roc_auc": 1.0
    },
    {
      "model": "RandomForestClassifier",
      "val_f1": 1.0,
      "val_roc_auc": 1.0,
      "test_f1": 1.0,
      "test_roc_auc": 1.0
    },
    {
      "model": "XGBClassifier",
      "val_f1": 0.7058823529411765,
      "val_roc_auc": 0.9996839443742098,
      "test_f1": 0.7692307692307693,
      "test_roc_auc": 0.9999288205566232
    },
    {
      "model": "SVC",
      "val_f1": 0.0,
      "val_roc_auc": 0.9469026548672568,
      "test_f1": 0.0,
      "test_roc_auc": 0.979002064203858
    },
    {
      "model": "GaussianNB",
      "val_f1": 0.25,
      "val_roc_auc": 0.5714285714285714,
      "test_f1": 0.0,
      "test_roc_auc": 0.5
    },
    {
      "model": "KNeighborsClassifier",
      "val_f1": 0.0,
      "val_roc_auc": 0.4947148475909538,
      "test_f1": 0.0,
      "test_roc_auc": 0.7475087194818136
    }
  ],
  "decision_summary": {
    "total_recommended_reorder_units": 144471.73586055712,
    "high_risk_rows": 1,
    "low_risk_rows": 5654,
    "transfer_candidates": 1,
    "hold_reduce_actions": 1382,
    "total_revenue_at_risk": 0.0
  },
  "top_reorder": [
    {
      "store_id": "S06",
      "product_id": "P110",
      "predicted_7_day_demand": 882.852,
      "safety_stock": 491.1710401986188,
      "reorder_quantity": 1204.023040198619,
      "risk_level": "LOW",
      "action": "NO ACTION"
    },
    {
      "store_id": "S03",
      "product_id": "P110",
      "predicted_7_day_demand": 797.308,
      "safety_stock": 432.42005695439485,
      "reorder_quantity": 1174.7280569543948,
      "risk_level": "LOW",
      "action": "NO ACTION"
    },
    {
      "store_id": "S08",
      "product_id": "P110",
      "predicted_7_day_demand": 801.904,
      "safety_stock": 498.53748661670073,
      "reorder_quantity": 1092.4414866167008,
      "risk_level": "LOW",
      "action": "NO ACTION"
    },
    {
      "store_id": "S02",
      "product_id": "P110",
      "predicted_7_day_demand": 855.296,
      "safety_stock": 263.8432304145089,
      "reorder_quantity": 983.139230414509,
      "risk_level": "LOW",
      "action": "NO ACTION"
    },
    {
      "store_id": "S10",
      "product_id": "P110",
      "predicted_7_day_demand": 759.4,
      "safety_stock": 453.2544907764421,
      "reorder_quantity": 963.654490776442,
      "risk_level": "LOW",
      "action": "NO ACTION"
    },
    {
      "store_id": "S10",
      "product_id": "P110",
      "predicted_7_day_demand": 832.892,
      "safety_stock": 405.6622076519738,
      "reorder_quantity": 922.554207651974,
      "risk_level": "LOW",
      "action": "NO ACTION"
    },
    {
      "store_id": "S03",
      "product_id": "P110",
      "predicted_7_day_demand": 771.024,
      "safety_stock": 311.6259777802143,
      "reorder_quantity": 893.6499777802144,
      "risk_level": "LOW",
      "action": "NO ACTION"
    },
    {
      "store_id": "S08",
      "product_id": "P110",
      "predicted_7_day_demand": 812.656,
      "safety_stock": 442.73824550139767,
      "reorder_quantity": 869.3942455013976,
      "risk_level": "LOW",
      "action": "NO ACTION"
    },
    {
      "store_id": "S06",
      "product_id": "P110",
      "predicted_7_day_demand": 869.172,
      "safety_stock": 0.0,
      "reorder_quantity": 869.172,
      "risk_level": "LOW",
      "action": "NO ACTION"
    },
    {
      "store_id": "S02",
      "product_id": "P110",
      "predicted_7_day_demand": 858.244,
      "safety_stock": 69.59662564230833,
      "reorder_quantity": 861.8406256423084,
      "risk_level": "LOW",
      "action": "NO ACTION"
    },
    {
      "store_id": "S06",
      "product_id": "P110",
      "predicted_7_day_demand": 855.908,
      "safety_stock": 0.0,
      "reorder_quantity": 855.908,
      "risk_level": "LOW",
      "action": "NO ACTION"
    },
    {
      "store_id": "S02",
      "product_id": "P110",
      "predicted_7_day_demand": 851.368,
      "safety_stock": 0.0,
      "reorder_quantity": 851.368,
      "risk_level": "LOW",
      "action": "NO ACTION"
    },
    {
      "store_id": "S09",
      "product_id": "P110",
      "predicted_7_day_demand": 788.504,
      "safety_stock": 433.18622133702144,
      "reorder_quantity": 849.6902213370215,
      "risk_level": "LOW",
      "action": "NO ACTION"
    },
    {
      "store_id": "S06",
      "product_id": "P110",
      "predicted_7_day_demand": 844.22,
      "safety_stock": 0.0,
      "reorder_quantity": 844.22,
      "risk_level": "LOW",
      "action": "NO ACTION"
    },
    {
      "store_id": "S03",
      "product_id": "P110",
      "predicted_7_day_demand": 835.14,
      "safety_stock": 0.0,
      "reorder_quantity": 835.14,
      "risk_level": "LOW",
      "action": "NO ACTION"
    }
  ],
  "volatility_bands": {
    "moderate": 903,
    "stable": 271,
    "high": 21,
    "nan": 4
  },
  "ablation": [
    {
      "experiment": "Experiment A",
      "features": 22,
      "val_mae": 11.285872191904174,
      "val_r2": 0.9744374182871444,
      "test_r2": 0.966914362427559
    },
    {
      "experiment": "Experiment B",
      "features": 32,
      "val_mae": 11.234446646835764,
      "val_r2": 0.974722936601976,
      "test_r2": 0.965473423590378
    },
    {
      "experiment": "Experiment C",
      "features": 30,
      "val_mae": 11.257818762067483,
      "val_r2": 0.9743083015736071,
      "test_r2": 0.9669070344441026
    },
    {
      "experiment": "Experiment D",
      "features": 39,
      "val_mae": 10.232201317716774,
      "val_r2": 0.9765106162217984,
      "test_r2": 0.9670696767057172
    },
    {
      "experiment": "Experiment E",
      "features": 57,
      "val_mae": 10.00458557344269,
      "val_r2": 0.9773468664635916,
      "test_r2": 0.9667326038855024
    }
  ]
};