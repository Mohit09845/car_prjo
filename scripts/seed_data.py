from model.car_model import Car, PriceRange, Engine, EngineOption, FuelTank, Dimensions, Safety
from model.variant_model import Variant

from database.connection import get_db


# ═══════════════════════════════════════════════════════════════════════════════
#  CAR  DATA  (one entry per model)
# ═══════════════════════════════════════════════════════════════════════════════

CARS = [

    # ── Maruti Suzuki Swift ───────────────────────────────────────────────────
    {
        "make":  "Maruti Suzuki",
        "model": "Swift",
        "type":  "Hatchback",
        "price_range_inr": {
            "min_ex_showroom": 578900,
            "max_ex_showroom": 884900,
        },
        "engine": {
            "displacement_cc": 1197,
            "cylinders":       3,
            "fuel_types":      ["Petrol", "CNG"],
            "transmissions":   ["Manual", "AMT"],
        },
        "dimensions": {
            "length_mm":           3860,
            "width_mm":            1735,
            "height_mm":           1520,
            "wheelbase_mm":        2450,
            "ground_clearance_mm": 163,
            "boot_space_litres":   265,
            "seating_capacity":    5,
            "doors":               5,
        },
        "safety": {
            "airbags":     6,
            "abs":         True,
            "ebd":         True,
            "esc":         True,
            "hill_assist": True,
            "isofix":      True,
            "ncap_stars":  1,
        },
        "colours": [
            "Sizzling Red", "Luster Blue", "Novel Orange", "Bluish Black",
            "Pearl Arctic White", "Magma Grey", "Splendid Silver",
            "Dual Tone Red + Black", "Dual Tone Blue + Black",
            "Dual Tone White + Black",
        ],
        "user_rating":  4.5,
        "review_count": 501,
    },

    # ── Maruti Suzuki Wagon R ─────────────────────────────────────────────────
    {
        "make":  "Maruti Suzuki",
        "model": "Wagon R",
        "type":  "Hatchback",
        "price_range_inr": {
            "min_ex_showroom": 498900,
            "max_ex_showroom": 694900,
        },
        "engine": {
            "displacement_cc": [998, 1197],
            "cylinders":       [3, 4],
            "fuel_types":      ["Petrol", "CNG"],
            "transmissions":   ["Manual", "AMT", "AT"],
        },
        "dimensions": {
            "length_mm":           3655,
            "width_mm":            1620,
            "height_mm":           1675,
            "wheelbase_mm":        2435,
            "ground_clearance_mm": 165,
            "boot_space_litres":   341,
            "seating_capacity":    5,
            "doors":               5,
        },
        "safety": {
            "airbags":     6,
            "abs":         True,
            "ebd":         True,
            "esc":         True,
            "hill_assist": True,
            "isofix":      False,
            "ncap_stars":  1,
        },
        "colours": [
            "Superior White", "Silky Silver", "Magma Grey",
            "Gallant Red", "Nutmeg Brown", "Poolside Blue",
            "Midnight Black", "Dual Tone Magma Grey + Black",
            "Dual Tone Gallant Red + Black",
        ],
        "user_rating":  4.4,
        "review_count": 512,
    },

    # Maruti suzuki baleno
    {
        "make":  "Maruti Suzuki",
        "model": "Baleno",
        "type":  "Premium Hatchback",
        "price_range_inr": {
            "min_ex_showroom": 599000,
            "max_ex_showroom": 910000,
        },
        "engine": {
            "displacement_cc": 1197,
            "cylinders":       4,
            "fuel_types":      ["Petrol", "CNG"],
            "transmissions":   ["Manual", "AMT"],
        },
        "dimensions": {
            "length_mm":           3990,
            "width_mm":            1745,
            "height_mm":           1500,
            "wheelbase_mm":        2520,
            "ground_clearance_mm": 170,
            "boot_space_litres":   318,
            "seating_capacity":    5,
            "doors":               5,
        },
        "safety": {
            "airbags":     6,           # top variants; base Sigma has 2
            "abs":         True,
            "ebd":         True,
            "esc":         True,
            "hill_assist": True,
            "isofix":      True,
            "ncap_stars":  4,           # Bharat NCAP
        },
        "colours": [
            "Pearl Arctic White", "Opulent Red", "Grandeur Grey",
            "Luxe Beige", "Bluish Black", "Nexa Blue", "Splendid Silver",
        ],
        "user_rating":  4.4,
        "review_count": 699,
    },

    # Maruti suzuki brezza 
    {
        "make":  "Maruti Suzuki",
        "model": "Brezza",
        "type":  "Compact SUV",
        "price_range_inr": {
            "min_ex_showroom": 975000,
            "max_ex_showroom": 1280000,
        },
        "engine": {
            "displacement_cc": 1462,
            "cylinders":       4,
            "fuel_types":      ["Petrol", "CNG"],
            "transmissions":   ["Manual", "AT"],
        },
        "dimensions": {
            "length_mm":           3995,
            "width_mm":            1790,
            "height_mm":           1685,
            "wheelbase_mm":        2500,
            "ground_clearance_mm": 198,
            "boot_space_litres":   328,
            "seating_capacity":    5,
            "doors":               5,
        },
        "safety": {
            "airbags":     6,           # top variants; base VXi has 2
            "abs":         True,
            "ebd":         True,
            "esc":         True,
            "hill_assist": True,
            "isofix":      True,
            "ncap_stars":  4,           # Bharat NCAP
        },
        "colours": [
            "Pearl Arctic White", "Splendid Silver", "Grandeur Grey",
            "Sizzling Red", "Brave Khaki", "Magma Grey", "Bluish Black",
            "Exuberant Blue",
            "Dual Tone White + Black", "Dual Tone Red + Black",
            "Dual Tone Silver + Black", "Dual Tone Khaki + White",
        ],
        "user_rating":  4.6,
        "review_count": 824,
    },

    # Maruti Suzuki Jimny

    {
        "make":  "Maruti Suzuki",
        "model": "Jimny",
        "type":  "Lifestyle SUV",
        "price_range_inr": {
            "min_ex_showroom": 1231000,
            "max_ex_showroom": 1445000,
        },
        "engine": {
            "displacement_cc": 1462,
            "cylinders":       4,
            "fuel_types":      ["Petrol"],
            "transmissions":   ["Manual", "AT"],
            "drive_type":      "4WD",           # unique — all others are FWD
        },
        "dimensions": {
            "length_mm":           3985,
            "width_mm":            1645,
            "height_mm":           1720,
            "wheelbase_mm":        2590,
            "ground_clearance_mm": 210,         # kept — critical for an off-road SUV
            "boot_space_litres":   208,
            "seating_capacity":    4,            # Jimny seats 4, not 5
            "doors":               5,
        },
        "safety": {
            "airbags":              6,
            "abs":                  True,
            "ebd":                  True,
            "esc":                  True,
            "hill_assist":          True,
            "hill_descent_control": True,       # unique off-road feature
            "isofix":               True,
            "ncap_stars":           3,
        },
        "colours": [
            "White", "Red", "Grey", "Black", "Blue", "Yellow",
            "Red + Black", "Yellow + Black",
        ],
        "user_rating":  4.5,
        "review_count": 406,
    },

    #Maruti Suzuki Ertiga
    {
    "make":  "Maruti Suzuki",
    "model": "Ertiga",
    "type":  "MUV",
    "price_range_inr": {
        "min_ex_showroom": 864000,
        "max_ex_showroom": 1308000,
    },
    "engine": {
        "displacement_cc": 1462,
        "cylinders":       4,
        "fuel_types":      ["Petrol", "CNG"],
        "transmissions":   ["Manual", "AT"],
    },
    "dimensions": {
        "length_mm":           4395,
        "width_mm":            1735,
        "height_mm":           1690,
        "wheelbase_mm":        2740,
        "ground_clearance_mm": 185,
        "boot_space_litres":   209,
        "seating_capacity":    7,
        "doors":               5,
    },
    "safety": {
        "airbags":     4,
        "abs":         True,
        "ebd":         True,
        "esc":         True,
        "hill_assist": True,
        "isofix":      True,
        "ncap_stars":  3,
    },
    "colours": [
        "Pearl Arctic White",
        "Splendid Silver",
        "Grandeur Grey",
        "Auburn Red",
        "Magma Grey",
        "Midnight Black",
    ],
    "user_rating":  4.3,
    "review_count": 1120,
},

#Maruti Suzuki Xl6
{
    "make":  "Maruti Suzuki",
    "model": "XL6",
    "type":  "MUV",
    "price_range_inr": {
        "min_ex_showroom": 1156000,
        "max_ex_showroom": 1482000,
    },
    "engine": {
        "displacement_cc": 1462,
        "cylinders":       4,
        "fuel_types":      ["Petrol", "CNG"],
        "transmissions":   ["Manual", "AT"],
    },
    "dimensions": {
        "length_mm":           4445,
        "width_mm":            1775,
        "height_mm":           1700,
        "wheelbase_mm":        2740,
        "ground_clearance_mm": 185,
        "boot_space_litres":   209,
        "seating_capacity":    6,
        "doors":               5,
    },
    "safety": {
        "airbags":     4,
        "abs":         True,
        "ebd":         True,
        "esc":         True,
        "hill_assist": True,
        "isofix":      True,
        "ncap_stars":  3,
    },
    "colours": [
        "Nexa Blue", "Arctic White", "Grandeur Grey",
        "Opulent Red", "Splendid Silver", "Brave Khaki"
    ],
    "user_rating":  4.4,
    "review_count": 1050,
},

# Maruti Suzuki Grand Vitara
{
    "make":  "Maruti Suzuki",
    "model": "Grand Vitara",
    "type":  "SUV",
    "price_range_inr": {
        "min_ex_showroom": 1070000,
        "max_ex_showroom": 1990000,
    },
    "engine": {
        "displacement_cc": [1462, 1490],
        "cylinders":       4,
        "fuel_types":      ["Petrol", "CNG", "Hybrid"],
        "transmissions":   ["Manual", "AT", "e-CVT"],
    },
    "dimensions": {
        "length_mm":           4345,
        "width_mm":            1795,
        "height_mm":           1645,
        "wheelbase_mm":        2600,
        "ground_clearance_mm": 210,
        "boot_space_litres":   373,
        "seating_capacity":    5,
        "doors":               5,
    },
    "safety": {
        "airbags":     6,
        "abs":         True,
        "ebd":         True,
        "esc":         True,
        "hill_assist": True,
        "isofix":      True,
        "ncap_stars":  5,
    },
    "colours": [
        "Nexa Blue",
        "Grandeur Grey",
        "Arctic White",
        "Chestnut Brown",
        "Opulent Red",
        "Splendid Silver",
        "Midnight Black",
    ],
    "user_rating":  4.5,
    "review_count": 625,
},

# Maruti Suzuki Ignis
{
  "make": "Maruti Suzuki",
  "model": "Ignis",
  "type": "Hatchback",
  "price_range_inr": {
    "min_ex_showroom": 535000,
    "max_ex_showroom": 755000
  },
  "engine": {
    "displacement_cc": 1197,
    "cylinders": 4,
    "fuel_types": ["Petrol"],
    "transmissions": ["Manual", "AMT"]
  },
  "dimensions": {
    "length_mm": 3700,
    "width_mm": 1690,
    "height_mm": 1595,
    "wheelbase_mm": 2435,
    "ground_clearance_mm": 180,
    "boot_space_litres": 260,
    "seating_capacity": 5,
    "doors": 5
  },
  "safety": {
    "airbags": 2,
    "abs": True,
    "ebd": True,
    "esc": True,
    "hill_assist": True,
    "isofix": True,
    "ncap_stars": 3
  },
  "colours": [
    "Nexa Blue",
    "Lucent Orange",
    "Turquoise Blue",
    "Silky Silver",
    "Pearl Arctic White",
    "Glistening Grey",
    "Pearl Midnight Black"
  ],
  "user_rating": 4.3,
  "review_count": 420
},

# Maruti Suzuki Ciaz
{
  "make": "Maruti Suzuki",
  "model": "Ciaz",
  "type": "Sedan",
  "price_range_inr": {
    "min_ex_showroom": 930000,
    "max_ex_showroom": 1210000
  },
  "engine": {
    "displacement_cc": 1462,
    "cylinders": 4,
    "fuel_types": ["Petrol"],
    "transmissions": ["Manual", "Automatic"]
  },
  "dimensions": {
    "length_mm": 4490,
    "width_mm": 1730,
    "height_mm": 1485,
    "wheelbase_mm": 2650,
    "ground_clearance_mm": 170,
    "boot_space_litres": 510,
    "seating_capacity": 5,
    "doors": 4
  },
  "safety": {
    "airbags": 2,
    "abs": True,
    "ebd": True,
    "esc": True,
    "hill_assist": True,
    "isofix": True,
    "ncap_stars": 4
  },
  "colours": [
    "Nexa Blue",
    "Pearl Snow White",
    "Metallic Premium Silver",
    "Pearl Sangria Red",
    "Pearl Dignity Brown",
    "Pearl Midnight Black",
    "Metallic Magma Grey"
  ],
  "user_rating": 4.4,
  "review_count": 510
},

#Maruti Suzuki Alto K10
{
  "make": "Maruti Suzuki",
  "model": "Alto K10",
  "type": "Hatchback",
  "price_range_inr": {
    "min_ex_showroom": 399000,
    "max_ex_showroom": 590000
  },
  "engine": {
    "displacement_cc": 998,
    "cylinders": 3,
    "fuel_types": ["Petrol", "CNG"],
    "transmissions": ["Manual", "AMT"]
  },
  "dimensions": {
    "length_mm": 3530,
    "width_mm": 1490,
    "height_mm": 1520,
    "wheelbase_mm": 2380,
    "ground_clearance_mm": 160,
    "boot_space_litres": 214,
    "seating_capacity": 5,
    "doors": 5
  },
  "safety": {
    "airbags": 2,
    "abs": True,
    "ebd": True,
    "esc": False,
    "hill_assist": True,
    "isofix": False,
    "ncap_stars": 2
  },
  "colours": [
    "Solid White",
    "Silky Silver",
    "Granite Grey",
    "Sizzling Red",
    "Speedy Blue"
  ],
  "user_rating": 4.2,
  "review_count": 380
},

#Maruti Suzuki Alto Tour H1
{
    "make":  "Maruti Suzuki",
    "model": "Alto Tour H1",
    "type":  "Hatchback",
    "price_range_inr": {
        "min_ex_showroom": 400000,
        "max_ex_showroom": 482000,
    },
    "engine": {
        "displacement_cc": 998,
        "cylinders":       3,
        "fuel_types":      ["Petrol", "CNG"],
        "transmissions":   ["Manual"],
    },
    "dimensions": {
        "length_mm":           3530,
        "width_mm":            1490,
        "height_mm":           1520,
        "wheelbase_mm":        2380,
        "ground_clearance_mm": 160,
        "boot_space_litres":   214,
        "seating_capacity":    5,
        "doors":               5,
    },
    "safety": {
        "airbags":     2,
        "abs":         True,
        "ebd":         True,
        "esc":         False,
        "hill_assist": False,
        "isofix":      False,
        "ncap_stars":  0,
    },
    "colours": ["White"],
    "user_rating":  4.5,
    "review_count": 6,
},

#Maruti Suzuki Celerio
{
    "make":  "Maruti Suzuki",
    "model": "Celerio",
    "type":  "Hatchback",
    "price_range_inr": {
        "min_ex_showroom": 470000,
        "max_ex_showroom": 673000,
    },
    "engine": {
        "displacement_cc": 998,
        "cylinders":       3,
        "fuel_types":      ["Petrol", "CNG"],
        "transmissions":   ["Manual", "AMT"],
    },
    "dimensions": {
        "length_mm":           3695,
        "width_mm":            1655,
        "height_mm":           1555,
        "wheelbase_mm":        2435,
        "ground_clearance_mm": 170,
        "boot_space_litres":   313,
        "seating_capacity":    5,
        "doors":               5,
    },
    "safety": {
        "airbags":     2,
        "abs":         True,
        "ebd":         True,
        "esc":         False,
        "hill_assist": True,
        "isofix":      True,
        "ncap_stars":  0,
    },
    "colours": [
        "Arctic White",
        "Silky Silver",
        "Glistening Grey",
        "Speedy Blue",
        "Caffeine Brown",
        "Solid Fire Red",
    ],
    "user_rating":  4.1,
    "review_count": 390,
},

# S-Presso Model

{
    "make":  "Maruti Suzuki",
    "model": "S-Presso",
    "type":  "Hatchback",
    "price_range_inr": {
        "min_ex_showroom": 350000,
        "max_ex_showroom": 525000,
    },
    "engine": {
        "displacement_cc": 998,
        "cylinders":       3,
        "fuel_types":      ["Petrol", "CNG"],
        "transmissions":   ["Manual", "AMT"],
    },
    "dimensions": {
        "length_mm":           3565,
        "width_mm":            1520,
        "height_mm":           1567,
        "wheelbase_mm":        2380,
        "ground_clearance_mm": 180,
        "boot_space_litres":   240,
        "seating_capacity":    4,
        "doors":               5,
    },
    "safety": {
        "airbags":     2,
        "abs":         True,
        "ebd":         True,
        "esc":         False,
        "hill_assist": False,
        "isofix":      False,
        "ncap_stars":  1,
    },
    "colours": [
        "Solid White",
        "Metallic Silky Silver",
        "Metallic Granite Grey",
        "Sizzle Orange",
        "Starry Blue",
    ],
    "user_rating":  4.3,
    "review_count": 493,
},


#Suzuki Eeco
{
    "make":  "Maruti Suzuki",
    "model": "Eeco",
    "type":  "MUV",
    "price_range_inr": {
        "min_ex_showroom": 521000,
        "max_ex_showroom": 636000,
    },
    "engine": {
        "displacement_cc": 1197,
        "cylinders":       4,
        "fuel_types":      ["Petrol", "CNG"],
        "transmissions":   ["Manual"],
    },
    "dimensions": {
        "length_mm":           3675,
        "width_mm":            1475,
        "height_mm":           1825,
        "wheelbase_mm":        2350,
        "ground_clearance_mm": 160,
        "boot_space_litres":   540,
        "seating_capacity":    7,
        "doors":               5,
    },
    "safety": {
        "airbags":     2,
        "abs":         True,
        "ebd":         True,
        "esc":         True,
        "hill_assist": False,
        "isofix":      False,
        "ncap_stars":  0,
    },
    "colours": [
        "Solid White",
        "Metallic Silky Silver",
        "Metallic Glistening Grey",
        "Metallic Brisk Blue",
        "Bluish Black",
    ],
    "user_rating":  4.3,
    "review_count": 310,
},

# Suzuki Fronx model
{
    "make":  "Maruti Suzuki",
    "model": "Fronx",
    "type":  "SUV",
    "price_range_inr": {
        "min_ex_showroom": 685000,
        "max_ex_showroom": 1198000,
    },
    "engine": {
        "displacement_cc": [998, 1197],
        "cylinders":       4,
        "fuel_types":      ["Petrol", "CNG"],
        "transmissions":   ["Manual", "AMT", "AT"],
    },
    "dimensions": {
        "length_mm":           3995,
        "width_mm":            1765,
        "height_mm":           1550,
        "wheelbase_mm":        2520,
        "ground_clearance_mm": 190,
        "boot_space_litres":   308,
        "seating_capacity":    5,
        "doors":               5,
    },
    "safety": {
        "airbags":     6,
        "abs":         True,
        "ebd":         True,
        "esc":         True,
        "hill_assist": True,
        "isofix":      True,
        "ncap_stars":  0,
    },
    "colours": [
        "Arctic White",
        "Opulent Red",
        "Grandeur Grey",
        "Splendid Silver",
        "Earthen Brown",
        "Bluish Black",
        "Dual Tone Options"
    ],
    "user_rating":  4.5,
    "review_count": 749,
},
    
]


# ═══════════════════════════════════════════════════════════════════════════════
#  VARIANT  DATA
# ═══════════════════════════════════════════════════════════════════════════════

VARIANTS = [

    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  SWIFT  VARIANTS
    # ╚══════════════════════════════════════════════════════════════════════════

    {
        "car_model": "Swift", "name": "LXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 578900, "price_on_road_inr": 647483,
        "mileage": 24.8, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "ABS + EBD + ESC", "Keyless Entry",
            "Push Button Start", "Rear Parking Sensors",
            "Digital Cluster", "Halogen Projector Headlamps",
            "Driver Attention Warning", "OTA Updates",
        ],
    },
    {
        "car_model": "Swift", "name": "VXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 658900, "price_on_road_inr": 754778,
        "mileage": 24.8, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "Cruise Control",
            "7-inch Touchscreen", "Wireless Android Auto & Apple CarPlay",
            "Wireless Phone Charging", "4-Speaker System",
            "LED Tail Lights", "Fog Lamps", "Leather Wrapped Steering",
        ],
    },
    {
        "car_model": "Swift", "name": "VXi Opt",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 684900, "price_on_road_inr": 790731,
        "mileage": 24.8, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "Auto Climate Control", "Cruise Control",
            "7-inch Touchscreen", "Wireless Android Auto & Apple CarPlay",
            "Valet Mode", "Remote Door Lock/Unlock", "Geo-fence Alert",
        ],
    },
    {
        "car_model": "Swift", "name": "VXi AMT",
        "fuel": "Petrol", "transmission": "AMT",
        "price_ex_showroom_inr": 703900, "price_on_road_inr": 813195,
        "mileage": 25.75, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "AMT Gearbox", "Auto Climate Control",
            "Cruise Control", "7-inch Touchscreen",
            "Wireless Android Auto & Apple CarPlay",
            "Valet Mode", "Remote Door Lock/Unlock",
        ],
    },
    {
        "car_model": "Swift", "name": "VXi Opt AMT",
        "fuel": "Petrol", "transmission": "AMT",
        "price_ex_showroom_inr": 729900, "price_on_road_inr": 830949,
        "mileage": 25.75, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "AMT Gearbox", "Auto Climate Control",
            "LED DRLs", "Idle Start-Stop System",
            "Valet Mode", "Geo-fence Alert",
        ],
    },
    {
        "car_model": "Swift", "name": "VXi CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 744900, "price_on_road_inr": 849814,
        "mileage": 32.85, "mileage_unit": "km/kg",
        "power_bhp": 68.80, "torque_nm": 101.8,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel", "Cruise Control",
            "7-inch Touchscreen", "Wireless Android Auto & Apple CarPlay",
            "Wireless Phone Charging", "Valet Mode",
        ],
    },
    {
        "car_model": "Swift", "name": "VXi Opt CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 770900, "price_on_road_inr": 875814,
        "mileage": 32.85, "mileage_unit": "km/kg",
        "power_bhp": 68.80, "torque_nm": 101.8,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel",
            "Auto Climate Control", "Idle Start-Stop System",
            "Valet Mode", "Geo-fence Alert",
        ],
    },
    {
        "car_model": "Swift", "name": "ZXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 752900, "price_on_road_inr": 866986,
        "mileage": 24.8, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "LED Headlights", "LED DRLs",
            "15-inch Alloy Wheels", "6-Speaker System",
            "Auto Climate Control", "Idle Start-Stop System",
            "Follow Me Home Headlamps",
        ],
    },
    {
        "car_model": "Swift", "name": "ZXi AMT",
        "fuel": "Petrol", "transmission": "AMT",
        "price_ex_showroom_inr": 797900, "price_on_road_inr": 904475,
        "mileage": 25.75, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "AMT Gearbox", "LED Headlights",
            "15-inch Alloy Wheels", "60:40 Split Rear Seat",
            "Surround Sense by ARKAMYS",
        ],
    },
    {
        "car_model": "Swift", "name": "ZXi CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 829900, "price_on_road_inr": 941236,
        "mileage": 32.85, "mileage_unit": "km/kg",
        "power_bhp": 68.80, "torque_nm": 101.8,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel",
            "LED Headlights", "15-inch Alloy Wheels",
            "Surround Sense by ARKAMYS", "60:40 Split Rear Seat",
        ],
    },
    {
        "car_model": "Swift", "name": "ZXi Plus",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 829900, "price_on_road_inr": 941236,
        "mileage": 24.8, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "9-inch SmartPlay Pro+ Touchscreen",
            "Rear Camera", "6+2 Speaker System",
            "15-inch Precision Cut Alloy Wheels",
            "Dual-Tone Roof Option", "Surround Sense by ARKAMYS",
        ],
    },
    {
        "car_model": "Swift", "name": "ZXi Plus DT",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 834900, "price_on_road_inr": 956991,
        "mileage": 24.8, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "9-inch SmartPlay Pro+ Touchscreen",
            "Dual-Tone Black Painted Roof", "Rear Camera",
            "Surround Sense by ARKAMYS",
        ],
    },
    {
        "car_model": "Swift", "name": "ZXi Plus AMT",
        "fuel": "Petrol", "transmission": "AMT",
        "price_ex_showroom_inr": 874900, "price_on_road_inr": 996991,
        "mileage": 25.75, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "AMT Gearbox",
            "9-inch SmartPlay Pro+ Touchscreen", "Rear Camera",
            "6+2 Speaker System", "15-inch Precision Cut Alloy Wheels",
        ],
    },
    {
        "car_model": "Swift", "name": "ZXi Plus AMT DT",
        "fuel": "Petrol", "transmission": "AMT",
        "price_ex_showroom_inr": 884900, "price_on_road_inr": 1012991,
        "mileage": 25.75, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "AMT Gearbox",
            "9-inch SmartPlay Pro+ Touchscreen",
            "Dual-Tone Black Painted Roof", "Rear Camera",
            "6+2 Speaker System", "15-inch Precision Cut Alloy Wheels",
        ],
    },

    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  WAGON R  VARIANTS
    # ╚══════════════════════════════════════════════════════════════════════════

    {
        "car_model": "Wagon R", "name": "LXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 498900, "price_on_road_inr": 557770,
        "mileage": 24.35, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89.0,
        "key_features": [
            "6 Airbags", "ABS + EBD + ESC", "Keyless Entry",
            "Rear Parking Sensors", "Idle Start-Stop",
            "Power Windows (Front)", "Halogen Headlamps",
        ],
    },
    {
        "car_model": "Wagon R", "name": "VXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 551900, "price_on_road_inr": 614386,
        "mileage": 24.35, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89.0,
        "key_features": [
            "6 Airbags", "Power Windows (Front + Rear)",
            "60:40 Split Rear Seat", "Keyless Entry",
            "Rear Parking Sensors", "Gear Shift Indicator",
        ],
    },
    {
        "car_model": "Wagon R", "name": "LXi CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 588900, "price_on_road_inr": 661412,
        "mileage": 34.05, "mileage_unit": "km/kg",
        "power_bhp": 55.92, "torque_nm": 82.1,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel",
            "Keyless Entry", "Rear Parking Sensors",
            "Idle Start-Stop", "60-litre CNG Tank",
        ],
    },
    {
        "car_model": "Wagon R", "name": "ZXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 595900, "price_on_road_inr": 666820,
        "mileage": 23.56, "mileage_unit": "kmpl",
        "power_bhp": 88.50, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "1197cc Engine", "Steering Mounted Controls",
            "Electrically Adjustable ORVMs", "Tilt Adjustable Steering",
            "60:40 Split Rear Seat", "Keyless Entry",
        ],
    },
    {
        "car_model": "Wagon R", "name": "VXi AMT",
        "fuel": "Petrol", "transmission": "AMT",
        "price_ex_showroom_inr": 596900, "price_on_road_inr": 662455,
        "mileage": 25.19, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89.0,
        "key_features": [
            "6 Airbags", "AMT Gearbox",
            "Power Windows (Front + Rear)", "60:40 Split Rear Seat",
            "Keyless Entry", "Rear Parking Sensors",
        ],
    },
    {
        "car_model": "Wagon R", "name": "VXi CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 642900, "price_on_road_inr": 724300,
        "mileage": 34.05, "mileage_unit": "km/kg",
        "power_bhp": 55.92, "torque_nm": 82.1,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel",
            "Power Windows (Front + Rear)", "60:40 Split Rear Seat",
            "Keyless Entry", "Rear Parking Sensors",
        ],
    },
    {
        "car_model": "Wagon R", "name": "ZXi AMT",
        "fuel": "Petrol", "transmission": "AMT",
        "price_ex_showroom_inr": 640900, "price_on_road_inr": 733279,
        "mileage": 24.43, "mileage_unit": "kmpl",
        "power_bhp": 88.50, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "1197cc Engine", "AMT Gearbox",
            "7-inch Touchscreen", "Android Auto & Apple CarPlay",
            "Fog Lights", "Alloy Wheels", "4 Speakers",
        ],
    },
    {
        "car_model": "Wagon R", "name": "ZXi Plus",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 638900, "price_on_road_inr": 731964,
        "mileage": 23.56, "mileage_unit": "kmpl",
        "power_bhp": 88.50, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "1197cc Engine",
            "7-inch Touchscreen", "Android Auto & Apple CarPlay",
            "Fog Lights", "14-inch Alloy Wheels",
            "4 Speakers", "Rear Parcel Tray",
        ],
    },
    {
        "car_model": "Wagon R", "name": "ZXi Plus AT",
        "fuel": "Petrol", "transmission": "AT",
        "price_ex_showroom_inr": 683900, "price_on_road_inr": 781431,
        "mileage": 24.43, "mileage_unit": "kmpl",
        "power_bhp": 88.50, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "1197cc Engine", "Automatic Transmission",
            "7-inch Touchscreen", "Android Auto & Apple CarPlay",
            "Fog Lights", "14-inch Alloy Wheels", "4 Speakers",
        ],
    },
    {
        "car_model": "Wagon R", "name": "ZXi Plus Dual Tone",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 689900, "price_on_road_inr": 791300,
        "mileage": 23.56, "mileage_unit": "kmpl",
        "power_bhp": 88.50, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "1197cc Engine", "Dual-Tone Paint",
            "7-inch Touchscreen", "Android Auto & Apple CarPlay",
            "Fog Lights", "14-inch Alloy Wheels", "4 Speakers",
        ],
    },
    {
        "car_model": "Wagon R", "name": "ZXi Plus AT Dual Tone",
        "fuel": "Petrol", "transmission": "AT",
        "price_ex_showroom_inr": 694900, "price_on_road_inr": 798300,
        "mileage": 24.43, "mileage_unit": "kmpl",
        "power_bhp": 88.50, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "1197cc Engine", "Automatic Transmission",
            "Dual-Tone Paint", "7-inch Touchscreen",
            "Android Auto & Apple CarPlay",
            "Fog Lights", "14-inch Alloy Wheels", "4 Speakers",
        ],
    },

    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  BALENO  VARIANTS
    # ╚══════════════════════════════════════════════════════════════════════════

    {
        "car_model": "Baleno", "name": "Sigma",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 599000, "price_on_road_inr": 665000,
        "mileage": 22.35, "mileage_unit": "kmpl",
        "power_bhp": 88.5, "torque_nm": 113.0,
        "key_features": [
            "2 Airbags", "ABS + EBD", "Rear Parking Sensors",
            "Power Windows (Front)", "Halogen Headlamps",
            "15-inch Wheels", "4-Star Bharat NCAP",
        ],
    },
    {
        "car_model": "Baleno", "name": "Delta",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 680000, "price_on_road_inr": 755000,
        "mileage": 22.35, "mileage_unit": "kmpl",
        "power_bhp": 88.5, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "ABS + EBD + ESC", "Keyless Entry",
            "Push Button Start", "Rear Parking Sensors",
            "7-inch Touchscreen", "Android Auto & Apple CarPlay",
        ],
    },
    {
        "car_model": "Baleno", "name": "Delta AMT",
        "fuel": "Petrol", "transmission": "AMT",
        "price_ex_showroom_inr": 730000, "price_on_road_inr": 810000,
        "mileage": 22.94, "mileage_unit": "kmpl",
        "power_bhp": 88.5, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "AMT Gearbox", "ABS + EBD + ESC",
            "Keyless Entry", "Push Button Start",
            "7-inch Touchscreen", "Android Auto & Apple CarPlay",
        ],
    },
    {
        "car_model": "Baleno", "name": "Delta CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 770000, "price_on_road_inr": 855000,
        "mileage": 30.61, "mileage_unit": "km/kg",
        "power_bhp": 76.43, "torque_nm": 98.5,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel", "ABS + EBD + ESC",
            "Keyless Entry", "Push Button Start",
            "7-inch Touchscreen", "Android Auto & Apple CarPlay",
        ],
    },
    {
        "car_model": "Baleno", "name": "Zeta",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 770000, "price_on_road_inr": 855000,
        "mileage": 22.35, "mileage_unit": "kmpl",
        "power_bhp": 88.5, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "Auto Climate Control", "Cruise Control",
            "9-inch Touchscreen", "Wireless Android Auto & Apple CarPlay",
            "Heads-Up Display", "LED Headlamps",
        ],
    },
    {
        "car_model": "Baleno", "name": "Zeta AMT",
        "fuel": "Petrol", "transmission": "AMT",
        "price_ex_showroom_inr": 820000, "price_on_road_inr": 910000,
        "mileage": 22.94, "mileage_unit": "kmpl",
        "power_bhp": 88.5, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "AMT Gearbox", "Auto Climate Control",
            "9-inch Touchscreen", "Wireless Android Auto & Apple CarPlay",
            "Heads-Up Display", "LED Headlamps",
        ],
    },
    {
        "car_model": "Baleno", "name": "Zeta CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 830000, "price_on_road_inr": 922000,
        "mileage": 30.61, "mileage_unit": "km/kg",
        "power_bhp": 76.43, "torque_nm": 98.5,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel", "Auto Climate Control",
            "9-inch Touchscreen", "Wireless Android Auto & Apple CarPlay",
            "Heads-Up Display",
        ],
    },
    {
        "car_model": "Baleno", "name": "Alpha",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 860000, "price_on_road_inr": 955000,
        "mileage": 22.35, "mileage_unit": "kmpl",
        "power_bhp": 88.5, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "Auto Climate Control", "Cruise Control",
            "9-inch Touchscreen", "Wireless Android Auto & Apple CarPlay",
            "Heads-Up Display", "360-Degree Camera",
            "6-Speaker ARKAMYS Sound System", "Tilt & Telescopic Steering",
        ],
    },
    {
        "car_model": "Baleno", "name": "Alpha AMT",
        "fuel": "Petrol", "transmission": "AMT",
        "price_ex_showroom_inr": 910000, "price_on_road_inr": 1010000,
        "mileage": 22.94, "mileage_unit": "kmpl",
        "power_bhp": 88.5, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "AMT Gearbox", "Auto Climate Control",
            "9-inch Touchscreen", "Wireless Android Auto & Apple CarPlay",
            "Heads-Up Display", "360-Degree Camera",
            "6-Speaker ARKAMYS Sound System", "Tilt & Telescopic Steering",
        ],
    },
 
    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  BREZZA  VARIANTS
    # ╚══════════════════════════════════════════════════════════════════════════

    {
        "car_model": "Brezza", "name": "VXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 975000, "price_on_road_inr": 1070000,
        "mileage": 20.15, "mileage_unit": "kmpl",
        "power_bhp": 102.0, "torque_nm": 136.8,
        "key_features": [
            "2 Airbags", "Smart Hybrid Engine", "ABS + EBD + ESC",
            "LED Projector Headlamps", "Cruise Control", "Keyless Entry",
            "7-inch Touchscreen", "Android Auto & Apple CarPlay",
            "4 Speakers", "Fog Lights",
        ],
    },
    {
        "car_model": "Brezza", "name": "ZXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1100000, "price_on_road_inr": 1210000,
        "mileage": 20.15, "mileage_unit": "kmpl",
        "power_bhp": 102.0, "torque_nm": 136.8,
        "key_features": [
            "6 Airbags", "Smart Hybrid Engine", "Auto Climate Control",
            "Push Button Start", "LED Headlamps with DRLs",
            "9-inch SmartPlay Pro+ Touchscreen",
            "Android Auto & Apple CarPlay", "6 Speakers", "Alloy Wheels",
        ],
    },
    {
        "car_model": "Brezza", "name": "VXi AT",
        "fuel": "Petrol", "transmission": "AT",
        "price_ex_showroom_inr": 1100000, "price_on_road_inr": 1220000,
        "mileage": 19.80, "mileage_unit": "kmpl",
        "power_bhp": 102.0, "torque_nm": 136.8,
        "key_features": [
            "2 Airbags", "Smart Hybrid Engine", "6-Speed Torque Converter",
            "ABS + EBD + ESC", "Cruise Control", "Keyless Entry",
            "LED Projector Headlamps", "7-inch Touchscreen",
            "Android Auto & Apple CarPlay",
        ],
    },
    {
        "car_model": "Brezza", "name": "ZXi AT",
        "fuel": "Petrol", "transmission": "AT",
        "price_ex_showroom_inr": 1200000, "price_on_road_inr": 1330000,
        "mileage": 19.80, "mileage_unit": "kmpl",
        "power_bhp": 102.0, "torque_nm": 136.8,
        "key_features": [
            "6 Airbags", "Smart Hybrid Engine", "6-Speed Torque Converter",
            "Auto Climate Control", "Push Button Start",
            "LED Headlamps with DRLs", "9-inch SmartPlay Pro+ Touchscreen",
            "6 Speakers", "Alloy Wheels",
        ],
    },
    {
        "car_model": "Brezza", "name": "ZXi CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 1200000, "price_on_road_inr": 1325000,
        "mileage": 25.51, "mileage_unit": "km/kg",
        "power_bhp": 87.8, "torque_nm": 121.5,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel", "Smart Hybrid Engine",
            "Auto Climate Control", "Push Button Start",
            "LED Headlamps with DRLs", "9-inch SmartPlay Pro+ Touchscreen",
            "6 Speakers", "Alloy Wheels",
        ],
    },
    {
        "car_model": "Brezza", "name": "ZXi CNG DT",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 1210000, "price_on_road_inr": 1340000,
        "mileage": 25.51, "mileage_unit": "km/kg",
        "power_bhp": 87.8, "torque_nm": 121.5,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel", "Dual-Tone Roof",
            "Auto Climate Control", "Push Button Start",
            "LED Headlamps with DRLs", "9-inch SmartPlay Pro+ Touchscreen",
            "6 Speakers", "Alloy Wheels",
        ],
    },
    {
        "car_model": "Brezza", "name": "ZXi AT DT",
        "fuel": "Petrol", "transmission": "AT",
        "price_ex_showroom_inr": 1230000, "price_on_road_inr": 1360000,
        "mileage": 19.80, "mileage_unit": "kmpl",
        "power_bhp": 102.0, "torque_nm": 136.8,
        "key_features": [
            "6 Airbags", "Smart Hybrid Engine", "6-Speed Torque Converter",
            "Dual-Tone Roof", "Auto Climate Control", "Push Button Start",
            "9-inch SmartPlay Pro+ Touchscreen", "6 Speakers", "Alloy Wheels",
        ],
    },
    {
        "car_model": "Brezza", "name": "ZXi Plus",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1250000, "price_on_road_inr": 1380000,
        "mileage": 20.15, "mileage_unit": "kmpl",
        "power_bhp": 102.0, "torque_nm": 136.8,
        "key_features": [
            "6 Airbags", "Smart Hybrid Engine", "360-Degree Camera",
            "Heads-Up Display", "Electric Sunroof", "Dual-Tone Roof",
            "Auto Climate Control", "9-inch SmartPlay Pro+ Touchscreen",
            "Wireless Charging", "ARKAMYS Surround Sound",
        ],
    },
    {
        "car_model": "Brezza", "name": "ZXi Plus DT",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1166300, "price_on_road_inr": 1353000,
        "mileage": 19.89, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 136.8,
        "key_features": [
            "6 Airbags", "Smart Hybrid Engine", "360-Degree Camera",
            "Heads-Up Display", "Electric Sunroof", "Dual-Tone Roof",
            "Cooled Glove Box", "Digital Cluster", "Leather Wrapped Steering",
            "9-inch SmartPlay Pro+ Touchscreen", "Wireless Charging",
        ],
    },
    {
        "car_model": "Brezza", "name": "ZXi Plus AT",
        "fuel": "Petrol", "transmission": "AT",
        "price_ex_showroom_inr": 1280000, "price_on_road_inr": 1410000,
        "mileage": 19.80, "mileage_unit": "kmpl",
        "power_bhp": 102.0, "torque_nm": 136.8,
        "key_features": [
            "6 Airbags", "Smart Hybrid Engine", "6-Speed Torque Converter",
            "360-Degree Camera", "Heads-Up Display", "Electric Sunroof",
            "Dual-Tone Roof", "Auto Climate Control", "Cooled Glove Box",
            "9-inch SmartPlay Pro+ Touchscreen", "Wireless Charging",
            "ARKAMYS Surround Sound",
        ],
    },

    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  JIMNY  VARIANTS
    # ╚══════════════════════════════════════════════════════════════════════════

    {
        "car_model": "Jimny", "name": "Zeta",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1231000, "price_on_road_inr": 1310000,
        "mileage": 16.94, "mileage_unit": "kmpl",
        "power_bhp": 103.0, "torque_nm": 134.2,
        "key_features": [
            "6 Airbags", "4WD AllGrip Pro", "Hill Assist",
            "Hill Descent Control", "ABS + EBD + ESC",
            "7-inch Touchscreen", "Android Auto & Apple CarPlay",
            "Keyless Entry", "Rear Parking Sensors",
        ],
    },
    {
        "car_model": "Jimny", "name": "Zeta AT",
        "fuel": "Petrol", "transmission": "AT",
        "price_ex_showroom_inr": 1337500, "price_on_road_inr": 1580000,
        "mileage": 16.39, "mileage_unit": "kmpl",
        "power_bhp": 103.0, "torque_nm": 134.2,
        "key_features": [
            "6 Airbags", "4WD AllGrip Pro", "4-Speed AT Gearbox",
            "Hill Assist", "Hill Descent Control",
            "7-inch Touchscreen", "Android Auto & Apple CarPlay",
            "Keyless Entry", "Push Button Start",
        ],
    },
    {
        "car_model": "Jimny", "name": "Alpha",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1323200, "price_on_road_inr": 1565000,
        "mileage": 16.94, "mileage_unit": "kmpl",
        "power_bhp": 103.0, "torque_nm": 134.2,
        "key_features": [
            "6 Airbags", "4WD AllGrip Pro", "Hill Assist",
            "Hill Descent Control", "Auto Climate Control",
            "Cruise Control", "LED Projector Headlamps", "LED Fog Lights",
            "9-inch SmartPlay Pro+ Touchscreen", "Alloy Wheels",
            "Rear Camera", "Digital Cluster",
        ],
    },
    {
        "car_model": "Jimny", "name": "Alpha Dual Tone",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1339000, "price_on_road_inr": 1585000,
        "mileage": 16.94, "mileage_unit": "kmpl",
        "power_bhp": 103.0, "torque_nm": 134.2,
        "key_features": [
            "6 Airbags", "4WD AllGrip Pro", "Dual-Tone Roof",
            "Hill Assist", "Hill Descent Control", "Auto Climate Control",
            "Cruise Control", "LED Projector Headlamps",
            "9-inch SmartPlay Pro+ Touchscreen", "Alloy Wheels",
        ],
    },
    {
        "car_model": "Jimny", "name": "Alpha AT",
        "fuel": "Petrol", "transmission": "AT",
        "price_ex_showroom_inr": 1429200, "price_on_road_inr": 1687000,
        "mileage": 16.39, "mileage_unit": "kmpl",
        "power_bhp": 103.0, "torque_nm": 134.2,
        "key_features": [
            "6 Airbags", "4WD AllGrip Pro", "4-Speed AT Gearbox",
            "Hill Assist", "Hill Descent Control", "Auto Climate Control",
            "Cruise Control", "LED Projector Headlamps", "LED Fog Lights",
            "9-inch SmartPlay Pro+ Touchscreen", "Alloy Wheels",
            "Rear Camera", "Push Button Start",
        ],
    },
    {
        "car_model": "Jimny", "name": "Alpha Dual Tone AT",
        "fuel": "Petrol", "transmission": "AT",
        "price_ex_showroom_inr": 1445000, "price_on_road_inr": 1705000,
        "mileage": 16.39, "mileage_unit": "kmpl",
        "power_bhp": 103.0, "torque_nm": 134.2,
        "key_features": [
            "6 Airbags", "4WD AllGrip Pro", "4-Speed AT Gearbox",
            "Dual-Tone Roof", "Hill Assist", "Hill Descent Control",
            "Auto Climate Control", "Cruise Control",
            "LED Projector Headlamps", "LED Fog Lights",
            "9-inch SmartPlay Pro+ Touchscreen", "Alloy Wheels",
            "Rear Camera", "Push Button Start",
        ],
    },

    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  Ertiga  VARIANTS
    # ╚══════════════════════════════════════════════════════════════════════════

    {
    "car_model": "Ertiga", "name": "LXi",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 864000, "price_on_road_inr": 996000,
    "mileage": 20.51, "mileage_unit": "kmpl",
    "power_bhp": 101.65, "torque_nm": 136.8,
    "key_features": [
        "2 Airbags", "ABS + EBD", "Rear Parking Sensors",
        "Power Windows", "Halogen Headlamps",
    ],
},
{
    "car_model": "Ertiga", "name": "VXi",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 978000, "price_on_road_inr": 1145000,
    "mileage": 20.51, "mileage_unit": "kmpl",
    "power_bhp": 101.65, "torque_nm": 136.8,
    "key_features": [
        "4 Airbags", "Keyless Entry", "Push Button Start",
        "7-inch Touchscreen", "Android Auto & Apple CarPlay",
    ],
},
{
    "car_model": "Ertiga", "name": "VXi AT",
    "fuel": "Petrol", "transmission": "AT",
    "price_ex_showroom_inr": 1088000, "price_on_road_inr": 1375000,
    "mileage": 20.30, "mileage_unit": "kmpl",
    "power_bhp": 101.65, "torque_nm": 136.8,
    "key_features": [
        "Automatic Transmission", "Cruise Control",
        "Touchscreen Infotainment", "Keyless Entry",
    ],
},
{
    "car_model": "Ertiga", "name": "VXi CNG",
    "fuel": "CNG", "transmission": "Manual",
    "price_ex_showroom_inr": 1073000, "price_on_road_inr": 1255000,
    "mileage": 26.11, "mileage_unit": "km/kg",
    "power_bhp": 87.83, "torque_nm": 121.5,
    "key_features": [
        "CNG + Petrol Bi-fuel", "Keyless Entry",
        "Touchscreen Infotainment", "Rear Parking Sensors",
    ],
},
{
    "car_model": "Ertiga", "name": "ZXi",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 1088000, "price_on_road_inr": 1308000,
    "mileage": 20.51, "mileage_unit": "kmpl",
    "power_bhp": 101.65, "torque_nm": 136.8,
    "key_features": [
        "6 Airbags", "Auto Climate Control", "Cruise Control",
        "LED Headlamps", "Alloy Wheels",
    ],
},
{
    "car_model": "Ertiga", "name": "ZXi AT",
    "fuel": "Petrol", "transmission": "AT",
    "price_ex_showroom_inr": 1198000, "price_on_road_inr": 1485000,
    "mileage": 20.30, "mileage_unit": "kmpl",
    "power_bhp": 101.65, "torque_nm": 136.8,
    "key_features": [
        "6 Airbags", "Automatic Transmission",
        "Cruise Control", "Touchscreen System",
    ],
},
{
    "car_model": "Ertiga", "name": "ZXi CNG",
    "fuel": "CNG", "transmission": "Manual",
    "price_ex_showroom_inr": 1183000, "price_on_road_inr": 1350000,
    "mileage": 26.11, "mileage_unit": "km/kg",
    "power_bhp": 87.83, "torque_nm": 121.5,
    "key_features": [
        "6 Airbags", "CNG + Petrol Bi-fuel",
        "Auto Climate Control", "Touchscreen System",
    ],
},
{
    "car_model": "Ertiga", "name": "ZXi Plus",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 1278000, "price_on_road_inr": 1347000,
    "mileage": 20.51, "mileage_unit": "kmpl",
    "power_bhp": 101.65, "torque_nm": 136.8,
    "key_features": [
        "6 Airbags", "360 Camera", "Cruise Control",
        "Touchscreen Infotainment", "Alloy Wheels",
    ],
},
{
    "car_model": "Ertiga", "name": "ZXi Plus AT",
    "fuel": "Petrol", "transmission": "AT",
    "price_ex_showroom_inr": 1308000, "price_on_road_inr": 1500000,
    "mileage": 20.30, "mileage_unit": "kmpl",
    "power_bhp": 101.65, "torque_nm": 136.8,
    "key_features": [
        "6 Airbags", "Automatic Transmission",
        "360 Camera", "Cruise Control",
        "Touchscreen Infotainment",
    ],
},

# ╔══════════════════════════════════════════════════════════════════════════
# ║  XL6  VARIANTS
# ╚══════════════════════════════════════════════════════════════════════════

  {
    "car_model": "XL6",
    "name": "Zeta",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1152000,
    "price_on_road_inr": 1358000,
    "mileage": 20.97,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "6 Airbags", "360 Camera", "Cruise Control",
      "Touchscreen Infotainment", "Alloy Wheels"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Zeta CNG",
    "fuel": "CNG",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1243000,
    "price_on_road_inr": 1450000,
    "mileage": 26.32,
    "mileage_unit": "km/kg",
    "power_bhp": 87.83,
    "torque_nm": 121.5,
    "key_features": [
      "Dual Fuel System", "6 Airbags",
      "Touchscreen Infotainment", "Alloy Wheels"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Alpha",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1249000,
    "price_on_road_inr": 1455000,
    "mileage": 20.97,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "Leather Upholstery", "Ventilated Seats",
      "360 Camera", "Cruise Control", "6 Airbags"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Zeta AT",
    "fuel": "Petrol",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1268000,
    "price_on_road_inr": 1475000,
    "mileage": 20.27,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "Automatic Transmission", "6 Airbags",
      "Cruise Control", "Touchscreen Infotainment"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Alpha AT",
    "fuel": "Petrol",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1348000,
    "price_on_road_inr": 1560000,
    "mileage": 20.27,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "Leather Upholstery", "Ventilated Seats",
      "Automatic Transmission", "360 Camera", "6 Airbags"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Alpha Plus",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1378000,
    "price_on_road_inr": 1590000,
    "mileage": 20.97,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "Dual Tone Exterior", "Leather Upholstery",
      "Ventilated Seats", "360 Camera", "6 Airbags"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Alpha Plus Dual Tone",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1398000,
    "price_on_road_inr": 1610000,
    "mileage": 20.97,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "Dual Tone Paint", "Leather Upholstery",
      "Ventilated Seats", "Cruise Control", "6 Airbags"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Alpha Plus AT",
    "fuel": "Petrol",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1428000,
    "price_on_road_inr": 1640000,
    "mileage": 20.27,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "Automatic Transmission", "Dual Tone Exterior",
      "Leather Upholstery", "Ventilated Seats", "6 Airbags"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Alpha Plus AT Dual Tone",
    "fuel": "Petrol",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1448000,
    "price_on_road_inr": 1660000,
    "mileage": 20.27,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "Dual Tone Paint", "Automatic Transmission",
      "Leather Upholstery", "Ventilated Seats", "6 Airbags"
    ]
  },

  # ╔══════════════════════════════════════════════════════════════════════════
  # ║  Grand Vitara  VARIANTS
  # ╚══════════════════════════════════════════════════════════════════════════

  {
    "car_model": "Grand Vitara",
    "name": "Sigma",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1077000,
    "price_on_road_inr": 1216000,
    "mileage": 21.11,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "Halogen Projector Headlamps",
      "LED DRLs",
      "17-inch Wheels with Covers",
      "Push Button Start",
      "Auto AC with Rear Vents",
      "6 Airbags"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Delta",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1210000,
    "price_on_road_inr": 1350000,
    "mileage": 21.11,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "Cruise Control",
      "Steering Mounted Controls",
      "7-inch Touchscreen",
      "Rear Parking Camera",
      "Suzuki Connect",
      "Tyre Pressure Monitoring System"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Delta AT",
    "fuel": "Petrol",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1345000,
    "price_on_road_inr": 1490000,
    "mileage": 20.58,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "Automatic Transmission",
      "Cruise Control",
      "Rear Parking Camera",
      "Suzuki Connect"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Delta CNG",
    "fuel": "CNG",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1300000,
    "price_on_road_inr": 1450000,
    "mileage": 26.6,
    "mileage_unit": "km/kg",
    "power_bhp": 87.83,
    "torque_nm": 121.5,
    "key_features": [
      "Factory-fit CNG Kit",
      "Cruise Control",
      "7-inch Touchscreen",
      "Rear Parking Camera"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Zeta",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1370000,
    "price_on_road_inr": 1520000,
    "mileage": 21.11,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "LED Headlamps",
      "Painted Alloy Wheels",
      "Ventilated Seats",
      "9-inch Touchscreen",
      "Premium 6-speaker Audio",
      "Panoramic Sunroof (Optional)"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Zeta CNG",
    "fuel": "CNG",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1525000,
    "price_on_road_inr": 1680000,
    "mileage": 26.6,
    "mileage_unit": "km/kg",
    "power_bhp": 87.83,
    "torque_nm": 121.5,
    "key_features": [
      "Factory-fit CNG Kit",
      "Ventilated Seats",
      "9-inch Touchscreen",
      "Panoramic Sunroof (Optional)"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Zeta+ Hybrid CVT",
    "fuel": "Petrol Hybrid",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1630000,
    "price_on_road_inr": 1800000,
    "mileage": 27.97,
    "mileage_unit": "kmpl",
    "power_bhp": 115.5,
    "torque_nm": 141,
    "key_features": [
      "Strong Hybrid Powertrain",
      "EV Mode",
      "Digital Instrument Cluster",
      "Ventilated Seats",
      "Panoramic Sunroof"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Alpha",
    "fuel": "Petrol",
    "transmission": "Manual/Automatic/AWD",
    "price_ex_showroom_inr": 1475000,
    "price_on_road_inr": 1650000,
    "mileage": 19.2,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "AWD Option",
      "Leatherette Seats",
      "8-way Powered Driver Seat",
      "Head-up Display",
      "360-degree Camera",
      "Panoramic Sunroof (Optional)"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Alpha+ Hybrid CVT",
    "fuel": "Petrol Hybrid",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1720000,
    "price_on_road_inr": 1972000,
    "mileage": 27.97,
    "mileage_unit": "kmpl",
    "power_bhp": 115.5,
    "torque_nm": 141,
    "key_features": [
      "Strong Hybrid Powertrain",
      "Leatherette Seats",
      "Head-up Display",
      "360-degree Camera",
      "Panoramic Sunroof"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Alpha Plus Opt Hybrid CVT DT",
    "fuel": "Petrol Hybrid",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1972000,
    "price_on_road_inr": 2200000,
    "mileage": 27.97,
    "mileage_unit": "kmpl",
    "power_bhp": 115.5,
    "torque_nm": 141,
    "key_features": ["Strong Hybrid", "Dual Tone Paint", "Panoramic Sunroof", "360-degree Camera", "Leatherette Seats"]
  },

    # Ignis variants
    {
    "car_model": "Ignis", "name": "Sigma",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 535000, "price_on_road_inr": 597000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "Dual Front Airbags", "ABS + EBD",
        "Manual AC", "Front Power Windows"
    ],
},
{
    "car_model": "Ignis", "name": "Delta",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 584000, "price_on_road_inr": 640000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "Bluetooth Audio", "Steering Mounted Controls",
        "Keyless Entry", "Rear Power Windows"
    ],
},
{
    "car_model": "Ignis", "name": "Delta AMT",
    "fuel": "Petrol", "transmission": "AMT",
    "price_ex_showroom_inr": 629000, "price_on_road_inr": 690000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "AMT Gearbox", "Hill Hold Assist",
        "Bluetooth Audio", "Steering Mounted Controls"
    ],
},
{
    "car_model": "Ignis", "name": "Delta Dual Tone AMT",
    "fuel": "Petrol", "transmission": "AMT",
    "price_ex_showroom_inr": 629000, "price_on_road_inr": 690000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "Dual Tone Exterior", "AMT Gearbox",
        "Hill Hold Assist", "Bluetooth Audio"
    ],
},
{
    "car_model": "Ignis", "name": "Zeta",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 638000, "price_on_road_inr": 700000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "15-inch Alloy Wheels", "Fog Lamps",
        "7-inch Touchscreen", "Push Button Start"
    ],
},
{
    "car_model": "Ignis", "name": "Zeta AMT",
    "fuel": "Petrol", "transmission": "AMT",
    "price_ex_showroom_inr": 683000, "price_on_road_inr": 745000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "AMT Gearbox", "15-inch Alloy Wheels",
        "7-inch Touchscreen", "Push Button Start"
    ],
},
{
    "car_model": "Ignis", "name": "Alpha",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 705000, "price_on_road_inr": 770000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "LED Projector Headlamps", "Automatic Climate Control",
        "Rearview Camera", "Height Adjustable Driver Seat"
    ],
},
{
    "car_model": "Ignis", "name": "Alpha AMT",
    "fuel": "Petrol", "transmission": "AMT",
    "price_ex_showroom_inr": 755000, "price_on_road_inr": 820000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "AMT Gearbox", "LED Projector Headlamps",
        "Automatic Climate Control", "Rearview Camera"
    ],
},
{
    "car_model": "Ignis", "name": "Alpha Dual Tone AMT",
    "fuel": "Petrol", "transmission": "AMT",
    "price_ex_showroom_inr": 755000, "price_on_road_inr": 820000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "Dual Tone Exterior", "AMT Gearbox",
        "LED Projector Headlamps", "Automatic Climate Control"
    ],
},

    #Ciaz variants
  {
    "car_model": "Ciaz",
    "name": "Sigma MT",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 909000,
    "price_on_road_inr": 1012800,
    "mileage": 20.65,
    "mileage_unit": "kmpl",
    "power_bhp": 103.25,
    "torque_nm": 138,
    "key_features": [
      "Dual Front Airbags",
      "ABS with EBD",
      "Manual AC",
      "Front Power Windows"
    ]
  },
  {
    "car_model": "Ciaz",
    "name": "Delta MT",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 965000,
    "price_on_road_inr": 1073000,
    "mileage": 20.65,
    "mileage_unit": "kmpl",
    "power_bhp": 103.25,
    "torque_nm": 138,
    "key_features": [
      "Keyless Entry",
      "Bluetooth Audio",
      "Steering Mounted Controls",
      "Rear Power Windows"
    ]
  },
  {
    "car_model": "Ciaz",
    "name": "Delta AT",
    "fuel": "Petrol",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1073000,
    "price_on_road_inr": 1185000,
    "mileage": 20.04,
    "mileage_unit": "kmpl",
    "power_bhp": 103.25,
    "torque_nm": 138,
    "key_features": [
      "Automatic Transmission",
      "Cruise Control",
      "Bluetooth Audio",
      "Rear Parking Camera"
    ]
  },
  {
    "car_model": "Ciaz",
    "name": "Zeta MT",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1005000,
    "price_on_road_inr": 1115000,
    "mileage": 20.65,
    "mileage_unit": "kmpl",
    "power_bhp": 103.25,
    "torque_nm": 138,
    "key_features": [
      "LED Projector Headlamps",
      "16-inch Alloy Wheels",
      "7-inch Touchscreen Infotainment",
      "Rear Sunshade"
    ]
  },
  {
    "car_model": "Ciaz",
    "name": "Zeta AT",
    "fuel": "Petrol",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1110000,
    "price_on_road_inr": 1225000,
    "mileage": 20.04,
    "mileage_unit": "kmpl",
    "power_bhp": 103.25,
    "torque_nm": 138,
    "key_features": [
      "Automatic Transmission",
      "LED Projector Headlamps",
      "16-inch Alloy Wheels",
      "7-inch Touchscreen Infotainment"
    ]
  },
  {
    "car_model": "Ciaz",
    "name": "Alpha MT",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1082000,
    "price_on_road_inr": 1195000,
    "mileage": 20.65,
    "mileage_unit": "kmpl",
    "power_bhp": 103.25,
    "torque_nm": 138,
    "key_features": [
      "Leather Upholstery",
      "Cruise Control",
      "Rear Parking Camera",
      "LED Projector Headlamps",
      "Automatic Climate Control"
    ]
  },
  {
    "car_model": "Ciaz",
    "name": "Alpha AT",
    "fuel": "Petrol",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1188000,
    "price_on_road_inr": 1310000,
    "mileage": 20.04,
    "mileage_unit": "kmpl",
    "power_bhp": 103.25,
    "torque_nm": 138,
    "key_features": [
      "Automatic Transmission",
      "Leather Upholstery",
      "Cruise Control",
      "Rear Parking Camera",
      "Automatic Climate Control"
    ]
  },

  #Alto K10 Variants
  {
    "car_model": "Alto K10", "name": "STD",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 370000, "price_on_road_inr": 415000,
    "mileage": 24.39, "mileage_unit": "kmpl",
    "power_bhp": 65.71, "torque_nm": 89,
    "key_features": [
        "Dual Airbags", "ABS + EBD",
        "Rear Parking Sensors"
    ],
},
{
    "car_model": "Alto K10", "name": "LXi",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 400000, "price_on_road_inr": 453000,
    "mileage": 24.39, "mileage_unit": "kmpl",
    "power_bhp": 65.71, "torque_nm": 89,
    "key_features": [
        "Power Steering", "AC",
        "Keyless Entry", "Front Power Windows"
    ],
},
{
    "car_model": "Alto K10", "name": "VXi",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 450000, "price_on_road_inr": 509000,
    "mileage": 24.39, "mileage_unit": "kmpl",
    "power_bhp": 65.71, "torque_nm": 89,
    "key_features": [
        "6 Airbags", "Central Locking",
        "Bluetooth Audio", "Steering Controls"
    ],
},
{
    "car_model": "Alto K10", "name": "VXi Plus",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 500000, "price_on_road_inr": 562000,
    "mileage": 24.39, "mileage_unit": "kmpl",
    "power_bhp": 65.71, "torque_nm": 89,
    "key_features": [
        "Touchscreen Infotainment",
        "Android Auto & Apple CarPlay",
        "4 Speakers"
    ],
},
{
    "car_model": "Alto K10", "name": "VXi AT",
    "fuel": "Petrol", "transmission": "AMT",
    "price_ex_showroom_inr": 550000, "price_on_road_inr": 609000,
    "mileage": 24.90, "mileage_unit": "kmpl",
    "power_bhp": 65.71, "torque_nm": 89,
    "key_features": [
        "AMT Gearbox", "Hill Assist",
        "Touchscreen System"
    ],
},
{
    "car_model": "Alto K10", "name": "VXi Plus AT",
    "fuel": "Petrol", "transmission": "AMT",
    "price_ex_showroom_inr": 545000, "price_on_road_inr": 655000,
    "mileage": 24.90, "mileage_unit": "kmpl",
    "power_bhp": 65.71, "torque_nm": 89,
    "key_features": [
        "AMT Gearbox", "SmartPlay Studio",
        "Android Auto & Apple CarPlay",
        "4 Speakers"
    ],
},
{
    "car_model": "Alto K10", "name": "LXi CNG",
    "fuel": "CNG", "transmission": "Manual",
    "price_ex_showroom_inr": 482000, "price_on_road_inr": 545000,
    "mileage": 33.85, "mileage_unit": "km/kg",
    "power_bhp": 55.92, "torque_nm": 82.1,
    "key_features": [
        "CNG + Petrol Bi-fuel",
        "Dual Airbags", "ABS + EBD"
    ],
},
{
    "car_model": "Alto K10", "name": "VXi CNG",
    "fuel": "CNG", "transmission": "Manual",
    "price_ex_showroom_inr": 568000, "price_on_road_inr": 635000,
    "mileage": 33.85, "mileage_unit": "km/kg",
    "power_bhp": 55.92, "torque_nm": 82.1,
    "key_features": [
        "CNG + Petrol Bi-fuel",
        "Power Windows", "Keyless Entry"
    ],
},

# Alto Tour H1 Variants
  {
    "car_model": "Alto Tour H1",
    "name": "Petrol MT",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 400000,
    "price_on_road_inr": 437808,
    "mileage": 24.39,
    "mileage_unit": "kmpl",
    "power_bhp": 67.58,
    "torque_nm": 91.1,
    "key_features": [
      "Compact Hatchback Design",
      "Affordable Fleet-Friendly Pricing",
      "Manual Transmission",
      "Basic Safety Features",
      "High Fuel Efficiency"
    ]
  },
  {
    "car_model": "Alto Tour H1",
    "name": "CNG MT",
    "fuel": "CNG",
    "transmission": "Manual",
    "price_ex_showroom_inr": 482000,
    "price_on_road_inr": 540000,
    "mileage": 33.4,
    "mileage_unit": "km/kg",
    "power_bhp": 55.92,
    "torque_nm": 82.1,
    "key_features": [
      "Factory-Fitted CNG Kit",
      "Economical Running Costs",
      "Manual Transmission",
      "Compact Size for Easy Parking",
      "Enhanced Mileage for Fleet Use"
    ]
  },

  # Celerio variants
  {
    "car_model": "Celerio", "name": "LXi",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 470000, "price_on_road_inr": 530000,
    "mileage": 25.24, "mileage_unit": "kmpl",
    "power_bhp": 67.77, "torque_nm": 91.1,
    "key_features": [
        "Dual Airbags", "ABS + EBD",
        "Manual AC", "Front Power Windows"
    ],
},
{
    "car_model": "Celerio", "name": "VXi",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 516000, "price_on_road_inr": 580000,
    "mileage": 25.24, "mileage_unit": "kmpl",
    "power_bhp": 67.77, "torque_nm": 91.1,
    "key_features": [
        "Keyless Entry", "Steering Controls",
        "Bluetooth Audio", "Rear Power Windows"
    ],
},
{
    "car_model": "Celerio", "name": "VXi AMT",
    "fuel": "Petrol", "transmission": "AMT",
    "price_ex_showroom_inr": 561000, "price_on_road_inr": 630000,
    "mileage": 26.68, "mileage_unit": "kmpl",
    "power_bhp": 67.77, "torque_nm": 91.1,
    "key_features": [
        "AMT Gearbox", "Hill Assist",
        "Bluetooth Audio", "Steering Controls"
    ],
},
{
    "car_model": "Celerio", "name": "ZXi",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 571000, "price_on_road_inr": 640000,
    "mileage": 25.24, "mileage_unit": "kmpl",
    "power_bhp": 67.77, "torque_nm": 91.1,
    "key_features": [
        "Alloy Wheels", "Fog Lamps",
        "Touchscreen Infotainment", "Push Button Start"
    ],
},
{
    "car_model": "Celerio", "name": "VXi CNG",
    "fuel": "CNG", "transmission": "Manual",
    "price_ex_showroom_inr": 598000, "price_on_road_inr": 670000,
    "mileage": 34.43, "mileage_unit": "km/kg",
    "power_bhp": 55.92, "torque_nm": 82.1,
    "key_features": [
        "CNG + Petrol Bi-fuel",
        "Keyless Entry", "Power Windows"
    ],
},
{
    "car_model": "Celerio", "name": "ZXi AMT",
    "fuel": "Petrol", "transmission": "AMT",
    "price_ex_showroom_inr": 616000, "price_on_road_inr": 690000,
    "mileage": 26.00, "mileage_unit": "kmpl",
    "power_bhp": 67.77, "torque_nm": 91.1,
    "key_features": [
        "AMT Gearbox", "Touchscreen System",
        "Push Button Start", "Alloy Wheels"
    ],
},
{
    "car_model": "Celerio", "name": "ZXi Plus",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 628000, "price_on_road_inr": 700000,
    "mileage": 24.97, "mileage_unit": "kmpl",
    "power_bhp": 67.77, "torque_nm": 91.1,
    "key_features": [
        "Touchscreen Infotainment",
        "Android Auto & Apple CarPlay",
        "Alloy Wheels"
    ],
},
{
    "car_model": "Celerio", "name": "ZXi Plus AMT",
    "fuel": "Petrol", "transmission": "AMT",
    "price_ex_showroom_inr": 673000, "price_on_road_inr": 750000,
    "mileage": 26.00, "mileage_unit": "kmpl",
    "power_bhp": 67.77, "torque_nm": 91.1,
    "key_features": [
        "AMT Gearbox", "Touchscreen Infotainment",
        "Android Auto & Apple CarPlay",
        "Push Button Start"
    ],
},

# Spresso Variants
{
    "car_model": "S-Presso", "name": "STD",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 350000, "price_on_road_inr": 395000,
    "mileage": 24.12, "mileage_unit": "kmpl",
    "power_bhp": 65.71, "torque_nm": 89,
    "key_features": [
        "Dual Airbags", "ABS + EBD",
        "Manual AC"
    ],
},
{
    "car_model": "S-Presso", "name": "LXi",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 380000, "price_on_road_inr": 430000,
    "mileage": 24.12, "mileage_unit": "kmpl",
    "power_bhp": 65.71, "torque_nm": 89,
    "key_features": [
        "Power Steering", "Front Power Windows",
        "Central Locking"
    ],
},
{
    "car_model": "S-Presso", "name": "VXi",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 430000, "price_on_road_inr": 480000,
    "mileage": 24.76, "mileage_unit": "kmpl",
    "power_bhp": 65.71, "torque_nm": 89,
    "key_features": [
        "Keyless Entry", "Steering Controls",
        "Bluetooth Audio"
    ],
},
{
    "car_model": "S-Presso", "name": "LXi CNG",
    "fuel": "CNG", "transmission": "Manual",
    "price_ex_showroom_inr": 462000, "price_on_road_inr": 520000,
    "mileage": 32.73, "mileage_unit": "km/kg",
    "power_bhp": 55.92, "torque_nm": 82.1,
    "key_features": [
        "CNG + Petrol Bi-fuel",
        "Dual Airbags", "ABS + EBD"
    ],
},
{
    "car_model": "S-Presso", "name": "VXi Opt AT",
    "fuel": "Petrol", "transmission": "AMT",
    "price_ex_showroom_inr": 475000, "price_on_road_inr": 535000,
    "mileage": 25.30, "mileage_unit": "kmpl",
    "power_bhp": 65.71, "torque_nm": 89,
    "key_features": [
        "AMT Gearbox", "Hill Assist",
        "Steering Controls", "Bluetooth Audio"
    ],
},
{
    "car_model": "S-Presso", "name": "VXi Plus",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 480000, "price_on_road_inr": 540000,
    "mileage": 24.76, "mileage_unit": "kmpl",
    "power_bhp": 65.71, "torque_nm": 89,
    "key_features": [
        "Touchscreen Infotainment",
        "Android Auto & Apple CarPlay",
        "Alloy Wheels"
    ],
},
{
    "car_model": "S-Presso", "name": "VXi CNG",
    "fuel": "CNG", "transmission": "Manual",
    "price_ex_showroom_inr": 512000, "price_on_road_inr": 575000,
    "mileage": 32.73, "mileage_unit": "km/kg",
    "power_bhp": 55.92, "torque_nm": 82.1,
    "key_features": [
        "CNG + Petrol Bi-fuel",
        "Power Windows", "Keyless Entry"
    ],
},
{
    "car_model": "S-Presso", "name": "VXi Plus Opt AT",
    "fuel": "Petrol", "transmission": "AMT",
    "price_ex_showroom_inr": 525000, "price_on_road_inr": 590000,
    "mileage": 25.30, "mileage_unit": "kmpl",
    "power_bhp": 65.71, "torque_nm": 89,
    "key_features": [
        "AMT Gearbox", "Touchscreen Infotainment",
        "Android Auto & Apple CarPlay",
        "Steering Controls"
    ],
},

# Eeco Variants
{
    "car_model": "Eeco", "name": "5 Seater STD",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 521000, "price_on_road_inr": 585000,
    "mileage": 19.71, "mileage_unit": "kmpl",
    "power_bhp": 79.65, "torque_nm": 105.5,
    "key_features": [
        "Dual Airbags", "ABS + EBD",
        "Rear Parking Sensors"
    ],
},
{
    "car_model": "Eeco", "name": "6 Seater STD",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 547000, "price_on_road_inr": 610000,
    "mileage": 19.71, "mileage_unit": "kmpl",
    "power_bhp": 79.65, "torque_nm": 105.5,
    "key_features": [
        "6 Seater Layout", "Dual Airbags",
        "ABS + EBD"
    ],
},
{
    "car_model": "Eeco", "name": "5 Seater AC",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 554000, "price_on_road_inr": 620000,
    "mileage": 19.71, "mileage_unit": "kmpl",
    "power_bhp": 79.65, "torque_nm": 105.5,
    "key_features": [
        "Manual AC", "Cabin Air Filter",
        "Dual Airbags", "ABS + EBD"
    ],
},
{
    "car_model": "Eeco", "name": "5 Seater AC CNG",
    "fuel": "CNG", "transmission": "Manual",
    "price_ex_showroom_inr": 636000, "price_on_road_inr": 710000,
    "mileage": 26.78, "mileage_unit": "km/kg",
    "power_bhp": 70.67, "torque_nm": 95,
    "key_features": [
        "CNG + Petrol Bi-fuel",
        "Manual AC", "Dual Airbags",
        "ABS + EBD"
    ],
},

# Fronx Variants
{
    "car_model": "Fronx", "name": "Sigma",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 685000, "price_on_road_inr": 830696,
    "mileage": 21.79, "mileage_unit": "kmpl",
    "power_bhp": 89, "torque_nm": 113,
    "key_features": [
        "Dual Airbags", "ABS + EBD",
        "Manual AC", "Power Windows"
    ],
},
{
    "car_model": "Fronx", "name": "Delta",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 765000, "price_on_road_inr": 913705,
    "mileage": 21.79, "mileage_unit": "kmpl",
    "power_bhp": 89, "torque_nm": 113,
    "key_features": [
        "Keyless Entry", "Steering Controls",
        "Bluetooth Audio", "Rear Power Windows"
    ],
},
{
    "car_model": "Fronx", "name": "Sigma CNG",
    "fuel": "CNG", "transmission": "Manual",
    "price_ex_showroom_inr": 779000, "price_on_road_inr": 958658,
    "mileage": 28.51, "mileage_unit": "km/kg",
    "power_bhp": 76.43, "torque_nm": 98.5,
    "key_features": [
        "CNG + Petrol Bi-fuel",
        "Dual Airbags", "ABS + EBD"
    ],
},
{
    "car_model": "Fronx", "name": "Delta AMT",
    "fuel": "Petrol", "transmission": "AMT",
    "price_ex_showroom_inr": 815000, "price_on_road_inr": 970000,
    "mileage": 22.89, "mileage_unit": "kmpl",
    "power_bhp": 89, "torque_nm": 113,
    "key_features": [
        "AMT Gearbox", "Hill Assist",
        "Steering Controls", "Bluetooth Audio"
    ],
},
{
  "car_model": "FRONX",
  "name": "Delta CNG",
  "fuel": "CNG",
  "transmission": "Manual",
  "price_ex_showroom_inr": 859000,
  "price_on_road_inr": 980000,
  "mileage": 28.51,
  "mileage_unit": "km/kg",
  "power_bhp": 76.43,
  "torque_nm": 98.5,
  "key_features": [
    "Dual Front Airbags",
    "ABS with EBD",
    "7-inch Touchscreen Infotainment",
    "Android Auto & Apple CarPlay",
    "Steering Mounted Controls",
    "Manual Air Conditioner",
    "Rear Parking Sensors",
    "ISOFIX Child Seat Mounts",
    "Electrically Adjustable ORVMs",
    "LED DRLs"
  ]
},
{
    "car_model": "Fronx", "name": "Delta Plus",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 804000, "price_on_road_inr": 900000,
    "mileage": 21.79, "mileage_unit": "kmpl",
    "power_bhp": 89, "torque_nm": 113,
    "key_features": [
        "Touchscreen Infotainment",
        "Android Auto & Apple CarPlay",
        "Rear Camera"
    ],
},
{
    "car_model": "Fronx", "name": "Delta Plus AMT",
    "fuel": "Petrol", "transmission": "AMT",
    "price_ex_showroom_inr": 854000, "price_on_road_inr": 950000,
    "mileage": 22.89, "mileage_unit": "kmpl",
    "power_bhp": 89, "torque_nm": 113,
    "key_features": [
        "AMT Gearbox", "Touchscreen System",
        "Rear Camera", "Smart Features"
    ],
},
{
    "car_model": "Fronx", "name": "Delta Plus Turbo",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 892000, "price_on_road_inr": 1000000,
    "mileage": 21.50, "mileage_unit": "kmpl",
    "power_bhp": 98.69, "torque_nm": 147.6,
    "key_features": [
        "Turbo Engine", "Cruise Control",
        "Touchscreen Infotainment"
    ],
},
{
    "car_model": "Fronx", "name": "Zeta Turbo",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 971000, "price_on_road_inr": 1080000,
    "mileage": 21.50, "mileage_unit": "kmpl",
    "power_bhp": 98.69, "torque_nm": 147.6,
    "key_features": [
        "Cruise Control", "Alloy Wheels",
        "LED Headlamps", "Push Button Start"
    ],
},
{
    "car_model": "Fronx", "name": "Alpha Turbo",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 1056000, "price_on_road_inr": 1180000,
    "mileage": 21.50, "mileage_unit": "kmpl",
    "power_bhp": 98.69, "torque_nm": 147.6,
    "key_features": [
        "360 Camera", "Heads-Up Display",
        "Premium Sound System"
    ],
},
{
    "car_model": "Fronx", "name": "Zeta Turbo AT",
    "fuel": "Petrol", "transmission": "AT",
    "price_ex_showroom_inr": 1099000, "price_on_road_inr": 1230000,
    "mileage": 20.01, "mileage_unit": "kmpl",
    "power_bhp": 98.69, "torque_nm": 147.6,
    "key_features": [
        "Automatic Transmission", "Cruise Control",
        "LED Headlamps"
    ],
},
{
    "car_model": "Fronx", "name": "Alpha Turbo AT",
    "fuel": "Petrol", "transmission": "AT",
    "price_ex_showroom_inr": 1184000, "price_on_road_inr": 1320000,
    "mileage": 20.01, "mileage_unit": "kmpl",
    "power_bhp": 98.69, "torque_nm": 147.6,
    "key_features": [
        "Automatic Transmission", "360 Camera",
        "Heads-Up Display"
    ],
},
{
    "car_model": "Fronx", "name": "Alpha Turbo DT AT",
    "fuel": "Petrol", "transmission": "AT",
    "price_ex_showroom_inr": 1198000, "price_on_road_inr": 1340000,
    "mileage": 20.01, "mileage_unit": "kmpl",
    "power_bhp": 98.69, "torque_nm": 147.6,
    "key_features": [
        "Dual Tone Exterior", "360 Camera",
        "Heads-Up Display", "Premium Features"
    ],
},


]


# ═══════════════════════════════════════════════════════════════════════════════
#  INSERT  FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def insert_cars():
    db  = get_db()
    col = db["cars"]
    for car in CARS:
        exists = col.find_one({"make": car["make"], "model": car["model"]})
        if not exists:
            result = col.insert_one(car)
            print(f"✅ Car inserted : {car['make']} {car['model']} → {result.inserted_id}")
        else:
            print(f"⚠️  Skipped      : {car['make']} {car['model']} (already exists)")


def insert_variants():
    db           = get_db()
    cars_col     = db["cars"]
    variants_col = db["variants"]

    for v in VARIANTS:
        car = cars_col.find_one({"model": v["car_model"]})
        if not car:
            print(f"❌ Car not found : {v['car_model']} — skipping variant '{v['name']}'")
            continue

        exists = variants_col.find_one({"car_id": car["_id"], "name": v["name"]})
        if not exists:
            payload = {**v, "car_id": car["_id"]}
            payload.pop("car_model")
            result = variants_col.insert_one(payload)
            print(f"✅ Variant inserted : {v['car_model']} {v['name']} → {result.inserted_id}")
        else:
            print(f"⚠️  Skipped         : {v['car_model']} {v['name']} (already exists)")


# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    insert_cars()
    insert_variants()