from pydantic import ValidationError

from model.car_model import Car
from model.variant_model import VariantSeed

from database.connection import get_db


# ═══════════════════════════════════════════════════════════════════════════════
#  CAR  DATA  (one entry per model)
# ═══════════════════════════════════════════════════════════════════════════════

CARS = [
    # ── Maruti Suzuki Swift ───────────────────────────────────────────────────
    {
        "make": "Maruti Suzuki",
        "model": "Swift",
        "type": "Hatchback",
        "price_range_inr": {
            "min_ex_showroom": 579000,
            "max_ex_showroom": 880000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1197, "cylinders": 3, "fuel_type": "Petrol"},
                {"displacement_cc": 1197, "cylinders": 3, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual", "Automatic"]
        },
        "fuel_tank": {"petrol_litres": 37, "cng_litres": 55},
        "dimensions": {
            "length_mm": 3860,
            "width_mm": 1735,
            "height_mm": 1520,
            "wheelbase_mm": 2450,
            "ground_clearance_mm": 163,
            "boot_space_litres": 265,
            "seating_capacity": 5,
            "doors": 5
        },
        "safety": {
            "airbags": 6,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": True,
            "isofix": True,
            "ncap_stars": 1
        },
        "colours": [
            "Sizzling Red", "Luster Blue", "Novel Orange", "Bluish Black",
            "Pearl Arctic White", "Magma Grey", "Splendid Silver",
            "Dual Tone Red + Black", "Dual Tone Blue + Black",
            "Dual Tone White + Black"
        ],
        "user_rating": 4.5,
        "review_count": 501
    },
    {
        "make": "Maruti Suzuki",
        "model": "Wagon R",
        "type": "Hatchback",
        "price_range_inr": {
            "min_ex_showroom": 499000,
            "max_ex_showroom": 695000
        },
        "engine": {
            "options": [
                {"displacement_cc": 998, "cylinders": 3, "fuel_type": "Petrol"},
                {"displacement_cc": 998, "cylinders": 3, "fuel_type": "CNG"},
                {"displacement_cc": 1197, "cylinders": 4, "fuel_type": "Petrol"}
            ],
            "transmissions": ["Manual", "Automatic"]
        },
        "fuel_tank": {"petrol_litres": 32, "cng_litres": 60},
        "dimensions": {
            "length_mm": 3655,
            "width_mm": 1620,
            "height_mm": 1675,
            "wheelbase_mm": 2435,
            "ground_clearance_mm": 165,
            "boot_space_litres": 341,
            "seating_capacity": 5,
            "doors": 5
        },
        "safety": {
            "airbags": 6,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": True,
            "isofix": False,
            "ncap_stars": 1
        },
        "colours": [
            "Superior White", "Silky Silver", "Magma Grey",
            "Gallant Red", "Nutmeg Brown", "Poolside Blue",
            "Midnight Black", "Dual Tone Magma Grey + Black",
            "Dual Tone Gallant Red + Black"
        ],
        "user_rating": 4.4,
        "review_count": 512
    },
    {
        "make": "Maruti Suzuki",
        "model": "Baleno",
        "type": "Premium Hatchback",
        "price_range_inr": {
            "min_ex_showroom": 599000,
            "max_ex_showroom": 910000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1197, "cylinders": 4, "fuel_type": "Petrol"},
                {"displacement_cc": 1197, "cylinders": 4, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual", "Automatic"]
        },
        "fuel_tank": {"petrol_litres": 37, "cng_litres": 55},
        "dimensions": {
            "length_mm": 3990,
            "width_mm": 1745,
            "height_mm": 1500,
            "wheelbase_mm": 2520,
            "ground_clearance_mm": 170,
            "boot_space_litres": 318,
            "seating_capacity": 5,
            "doors": 5
        },
        "safety": {
            "airbags": 6,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": True,
            "isofix": True,
            "ncap_stars": 4
        },
        "colours": [
            "Pearl Arctic White", "Opulent Red", "Grandeur Grey",
            "Luxe Beige", "Bluish Black", "Nexa Blue", "Splendid Silver"
        ],
        "user_rating": 4.4,
        "review_count": 699
    },
    {
        "make": "Maruti Suzuki",
        "model": "Brezza",
        "type": "Compact SUV",
        "price_range_inr": {
            "min_ex_showroom": 826000,
            "max_ex_showroom": 1301000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1462, "cylinders": 4, "fuel_type": "Petrol"},
                {"displacement_cc": 1462, "cylinders": 4, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual", "Automatic"]
        },
        "fuel_tank": {"petrol_litres": 48, "cng_litres": 55},
        "dimensions": {
            "length_mm": 3995,
            "width_mm": 1790,
            "height_mm": 1685,
            "wheelbase_mm": 2500,
            "ground_clearance_mm": 198,
            "boot_space_litres": 328,
            "seating_capacity": 5,
            "doors": 5
        },
        "safety": {
            "airbags": 6,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": True,
            "isofix": True,
            "ncap_stars": 4
        },
        "colours": [
            "Pearl Arctic White", "Splendid Silver", "Grandeur Grey",
            "Sizzling Red", "Brave Khaki", "Magma Grey", "Bluish Black",
            "Exuberant Blue",
            "Dual Tone White + Black", "Dual Tone Red + Black",
            "Dual Tone Silver + Black", "Dual Tone Khaki + White"
        ],
        "user_rating": 4.6,
        "review_count": 824
    },
    {
        "make": "Maruti Suzuki",
        "model": "Jimny",
        "type": "Lifestyle SUV",
        "price_range_inr": {
            "min_ex_showroom": 1231000,
            "max_ex_showroom": 1445000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1462, "cylinders": 4, "fuel_type": "Petrol"}
            ],
            "transmissions": ["Manual", "Automatic"]
        },
        "fuel_tank": {"petrol_litres": 40},
        "dimensions": {
            "length_mm": 3985,
            "width_mm": 1645,
            "height_mm": 1720,
            "wheelbase_mm": 2590,
            "ground_clearance_mm": 210,
            "boot_space_litres": 208,
            "seating_capacity": 4,
            "doors": 5
        },
        "safety": {
            "airbags": 6,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": True,
            "isofix": True,
            "ncap_stars": 3
        },
        "colours": [
            "White", "Red", "Grey", "Black", "Blue", "Yellow",
            "Red + Black", "Yellow + Black"
        ],
        "user_rating": 4.5,
        "review_count": 406
    },
    {
        "make": "Maruti Suzuki",
        "model": "Ertiga",
        "type": "MUV",
        "price_range_inr": {
            "min_ex_showroom": 880000,
            "max_ex_showroom": 1294000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1462, "cylinders": 4, "fuel_type": "Petrol"},
                {"displacement_cc": 1462, "cylinders": 4, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual", "Automatic"]
        },
        "fuel_tank": {"petrol_litres": 45, "cng_litres": 60},
        "dimensions": {
            "length_mm": 4395,
            "width_mm": 1735,
            "height_mm": 1690,
            "wheelbase_mm": 2740,
            "ground_clearance_mm": 185,
            "boot_space_litres": 209,
            "seating_capacity": 7,
            "doors": 5
        },
        "safety": {
            "airbags": 4,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": True,
            "isofix": True,
            "ncap_stars": 3
        },
        "colours": [
            "Pearl Arctic White",
            "Splendid Silver",
            "Grandeur Grey",
            "Auburn Red",
            "Magma Grey",
            "Midnight Black"
        ],
        "user_rating": 4.3,
        "review_count": 1120
    },
    {
        "make": "Maruti Suzuki",
        "model": "XL6",
        "type": "MUV",
        "price_range_inr": {
            "min_ex_showroom": 1152000,
            "max_ex_showroom": 1447000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1462, "cylinders": 4, "fuel_type": "Petrol"},
                {"displacement_cc": 1462, "cylinders": 4, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual", "Automatic"]
        },
        "fuel_tank": {"petrol_litres": 45, "cng_litres": 60},
        "dimensions": {
            "length_mm": 4445,
            "width_mm": 1775,
            "height_mm": 1700,
            "wheelbase_mm": 2740,
            "ground_clearance_mm": 185,
            "boot_space_litres": 209,
            "seating_capacity": 6,
            "doors": 5
        },
        "safety": {
            "airbags": 4,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": True,
            "isofix": True,
            "ncap_stars": 3
        },
        "colours": [
            "Nexa Blue", "Arctic White", "Grandeur Grey",
            "Opulent Red", "Splendid Silver", "Brave Khaki"
        ],
        "user_rating": 4.4,
        "review_count": 1050
    },
    {
        "make": "Maruti Suzuki",
        "model": "Grand Vitara",
        "type": "SUV",
        "price_range_inr": {
            "min_ex_showroom": 1077000,
            "max_ex_showroom": 1972000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1462, "cylinders": 4, "fuel_type": "Petrol"},
                {"displacement_cc": 1462, "cylinders": 4, "fuel_type": "CNG"},
                {"displacement_cc": 1462, "cylinders": 4, "fuel_type": "Hybrid"},
                {"displacement_cc": 1490, "cylinders": 4, "fuel_type": "Petrol"},
                {"displacement_cc": 1490, "cylinders": 4, "fuel_type": "CNG"},
                {"displacement_cc": 1490, "cylinders": 4, "fuel_type": "Hybrid"}
            ],
            "transmissions": ["Manual", "Automatic", "CVT"]
        },
        "fuel_tank": {"petrol_litres": 45, "cng_litres": 55},
        "dimensions": {
            "length_mm": 4345,
            "width_mm": 1795,
            "height_mm": 1645,
            "wheelbase_mm": 2600,
            "ground_clearance_mm": 210,
            "boot_space_litres": 373,
            "seating_capacity": 5,
            "doors": 5
        },
        "safety": {
            "airbags": 6,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": True,
            "isofix": True,
            "ncap_stars": 5
        },
        "colours": [
            "Nexa Blue",
            "Grandeur Grey",
            "Arctic White",
            "Chestnut Brown",
            "Opulent Red",
            "Splendid Silver",
            "Midnight Black"
        ],
        "user_rating": 4.5,
        "review_count": 625
    },
    {
        "make": "Maruti Suzuki",
        "model": "Ignis",
        "type": "Hatchback",
        "price_range_inr": {
            "min_ex_showroom": 535000,
            "max_ex_showroom": 755000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1197, "cylinders": 4, "fuel_type": "Petrol"}
            ],
            "transmissions": ["Manual", "Automatic"]
        },
        "fuel_tank": {"petrol_litres": 32},
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
            "ncap_stars": 1
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
    {
        "make": "Maruti Suzuki",
        "model": "Ciaz",
        "type": "Sedan",
        "price_range_inr": {
            "min_ex_showroom": 909000,
            "max_ex_showroom": 1188000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1462, "cylinders": 4, "fuel_type": "Petrol"}
            ],
            "transmissions": ["Manual", "Automatic"]
        },
        "fuel_tank": {"petrol_litres": 43},
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
    {
        "make": "Maruti Suzuki",
        "model": "Alto K10",
        "type": "Hatchback",
        "price_range_inr": {
            "min_ex_showroom": 370000,
            "max_ex_showroom": 545000
        },
        "engine": {
            "options": [
                {"displacement_cc": 998, "cylinders": 3, "fuel_type": "Petrol"},
                {"displacement_cc": 998, "cylinders": 3, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual", "Automatic"]
        },
        "fuel_tank": {"petrol_litres": 35, "cng_litres": 55},
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
    {
        "make": "Maruti Suzuki",
        "model": "Alto Tour H1",
        "type": "Hatchback",
        "price_range_inr": {
            "min_ex_showroom": 400000,
            "max_ex_showroom": 482000
        },
        "engine": {
            "options": [
                {"displacement_cc": 998, "cylinders": 3, "fuel_type": "Petrol"},
                {"displacement_cc": 998, "cylinders": 3, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual"]
        },
        "fuel_tank": {"petrol_litres": 35, "cng_litres": 55},
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
            "hill_assist": False,
            "isofix": False,
            "ncap_stars": None
        },
        "colours": [
            "White"
        ],
        "user_rating": 4.5,
        "review_count": 6
    },
    {
        "make": "Maruti Suzuki",
        "model": "Celerio",
        "type": "Hatchback",
        "price_range_inr": {
            "min_ex_showroom": 470000,
            "max_ex_showroom": 673000
        },
        "engine": {
            "options": [
                {"displacement_cc": 998, "cylinders": 3, "fuel_type": "Petrol"},
                {"displacement_cc": 998, "cylinders": 3, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual", "Automatic"]
        },
        "fuel_tank": {"petrol_litres": 32, "cng_litres": 60},
        "dimensions": {
            "length_mm": 3695,
            "width_mm": 1655,
            "height_mm": 1555,
            "wheelbase_mm": 2435,
            "ground_clearance_mm": 170,
            "boot_space_litres": 313,
            "seating_capacity": 5,
            "doors": 5
        },
        "safety": {
            "airbags": 2,
            "abs": True,
            "ebd": True,
            "esc": False,
            "hill_assist": True,
            "isofix": True,
            "ncap_stars": None
        },
        "colours": [
            "Arctic White",
            "Silky Silver",
            "Glistening Grey",
            "Speedy Blue",
            "Caffeine Brown",
            "Solid Fire Red"
        ],
        "user_rating": 4.1,
        "review_count": 390
    },
    {
        "make": "Maruti Suzuki",
        "model": "S-Presso",
        "type": "Hatchback",
        "price_range_inr": {
            "min_ex_showroom": 350000,
            "max_ex_showroom": 525000
        },
        "engine": {
            "options": [
                {"displacement_cc": 998, "cylinders": 3, "fuel_type": "Petrol"},
                {"displacement_cc": 998, "cylinders": 3, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual", "Automatic"]
        },
        "fuel_tank": {"petrol_litres": 27, "cng_litres": 55},
        "dimensions": {
            "length_mm": 3565,
            "width_mm": 1520,
            "height_mm": 1567,
            "wheelbase_mm": 2380,
            "ground_clearance_mm": 180,
            "boot_space_litres": 240,
            "seating_capacity": 5,
            "doors": 5
        },
        "safety": {
            "airbags": 2,
            "abs": True,
            "ebd": True,
            "esc": False,
            "hill_assist": False,
            "isofix": False,
            "ncap_stars": 1
        },
        "colours": [
            "Solid White",
            "Metallic Silky Silver",
            "Metallic Granite Grey",
            "Sizzle Orange",
            "Starry Blue"
        ],
        "user_rating": 4.3,
        "review_count": 493
    },
    {
        "make": "Maruti Suzuki",
        "model": "Eeco",
        "type": "MUV",
        "price_range_inr": {
            "min_ex_showroom": 521000,
            "max_ex_showroom": 636000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1197, "cylinders": 4, "fuel_type": "Petrol"},
                {"displacement_cc": 1197, "cylinders": 4, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual"]
        },
        "fuel_tank": {"petrol_litres": 32, "cng_litres": 65},
        "dimensions": {
            "length_mm": 3675,
            "width_mm": 1475,
            "height_mm": 1825,
            "wheelbase_mm": 2350,
            "ground_clearance_mm": 160,
            "boot_space_litres": 540,
            "seating_capacity": 7,
            "doors": 5
        },
        "safety": {
            "airbags": 2,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": False,
            "isofix": False,
            "ncap_stars": None
        },
        "colours": [
            "Solid White",
            "Metallic Silky Silver",
            "Metallic Glistening Grey",
            "Metallic Brisk Blue",
            "Bluish Black"
        ],
        "user_rating": 4.3,
        "review_count": 310
    },
    {
        "make": "Maruti Suzuki",
        "model": "Fronx",
        "type": "SUV",
        "price_range_inr": {
            "min_ex_showroom": 685000,
            "max_ex_showroom": 1198000
        },
        "engine": {
            "options": [
                {"displacement_cc": 998, "cylinders": 3, "fuel_type": "Petrol"},
                {"displacement_cc": 1197, "cylinders": 4, "fuel_type": "Petrol"},
                {"displacement_cc": 1197, "cylinders": 4, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual", "Automatic"]
        },
        "fuel_tank": {"petrol_litres": 37, "cng_litres": 55},
        "dimensions": {
            "length_mm": 3995,
            "width_mm": 1765,
            "height_mm": 1550,
            "wheelbase_mm": 2520,
            "ground_clearance_mm": 190,
            "boot_space_litres": 308,
            "seating_capacity": 5,
            "doors": 5
        },
        "safety": {
            "airbags": 6,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": True,
            "isofix": True,
            "ncap_stars": None
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
        "user_rating": 4.5,
        "review_count": 749
    },
    {
        "make": "Maruti Suzuki",
        "model": "Dzire",
        "type": "Sedan",
        "price_range_inr": {
            "min_ex_showroom": 626000,
            "max_ex_showroom": 931000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1197, "cylinders": 3, "fuel_type": "Petrol"},
                {"displacement_cc": 1197, "cylinders": 3, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual", "Automatic"]
        },
        "fuel_tank": {"petrol_litres": 37, "cng_litres": 55},
        "dimensions": {
            "length_mm": 3995,
            "width_mm": 1735,
            "height_mm": 1520,
            "wheelbase_mm": 2450,
            "ground_clearance_mm": 170,
            "boot_space_litres": 378,
            "seating_capacity": 5,
            "doors": 4
        },
        "safety": {
            "airbags": 6,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": True,
            "isofix": True,
            "ncap_stars": 5
        },
        "colours": [
            "Gallant Red",
            "Alluring Blue",
            "Nutmeg Brown",
            "Bluish Black",
            "Arctic White",
            "Magma Grey",
            "Splendid Silver"
        ],
        "user_rating": 4.75,
        "review_count": 3800
    },
    {
        "make": "Maruti Suzuki",
        "model": "Invicto",
        "type": "MUV",
        "price_range_inr": {
            "min_ex_showroom": 2497000,
            "max_ex_showroom": 2861000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1987, "cylinders": 4, "fuel_type": "Hybrid"}
            ],
            "transmissions": ["Automatic"]
        },
        "fuel_tank": {"petrol_litres": 52},
        "dimensions": {
            "length_mm": 4755,
            "width_mm": 1845,
            "height_mm": 1795,
            "wheelbase_mm": 2850,
            "ground_clearance_mm": 185,
            "boot_space_litres": 239,
            "seating_capacity": 7,
            "doors": 5
        },
        "safety": {
            "airbags": 6,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": True,
            "isofix": True,
            "ncap_stars": None
        },
        "colours": [
            "Pearl Arctic White",
            "Splendid Silver",
            "Magma Grey",
            "Bluish Black",
            "Nexa Blue"
        ],
        "user_rating": 4.6,
        "review_count": 420
    },
    {
        "make": "Maruti Suzuki",
        "model": "Victoris",
        "type": "SUV",
        "price_range_inr": {
            "min_ex_showroom": 1050000,
            "max_ex_showroom": 1999000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1462, "cylinders": 4, "fuel_type": "Petrol"},
                {"displacement_cc": 1462, "cylinders": 4, "fuel_type": "CNG"},
                {"displacement_cc": 1490, "cylinders": 3, "fuel_type": "Hybrid"}
            ],
            "transmissions": ["Manual", "Automatic"]
        },
        "fuel_tank": {"petrol_litres": 45, "cng_litres": 55},
        "dimensions": {
            "length_mm": 4360,
            "width_mm": 1795,
            "height_mm": 1655,
            "wheelbase_mm": 2600,
            "ground_clearance_mm": 210,
            "boot_space_litres": 373,
            "seating_capacity": 5,
            "doors": 5
        },
        "safety": {
            "airbags": 6,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": True,
            "isofix": True,
            "ncap_stars": 5
        },
        "colours": [
            "Nexa Blue",
            "Splendid Silver",
            "Grandeur Grey",
            "Pearl Arctic White",
            "Bluish Black",
            "Opulent Red"
        ],
        "user_rating": 4.7,
        "review_count": 84
    },
    {
        "make": "Maruti Suzuki",
        "model": "e Vitara",
        "type": "Electric SUV",
        "price_range_inr": {
            "min_ex_showroom": 1599000,
            "max_ex_showroom": 2001000
        },
        "electric": {
            "battery_capacity_kwh": [49.0, 61.0],
            "range_km_arai_peak": 543,
            "peak_power_kw": 128.0
        },
        "dimensions": {
            "length_mm": 4275,
            "width_mm": 1800,
            "height_mm": 1640,
            "wheelbase_mm": 2700,
            "ground_clearance_mm": 180,
            "boot_space_litres": 306,
            "seating_capacity": 5,
            "doors": 5
        },
        "safety": {
            "airbags": 7,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": True,
            "isofix": True,
            "ncap_stars": None
        },
        "colours": [
            "Pearl Arctic White",
            "Splendid Silver",
            "Bluish Black",
            "Nexa Blue",
            "Grandeur Grey"
        ],
        "user_rating": 4.5,
        "review_count": 120
    },
    {
        "make": "Maruti Suzuki",
        "model": "Dzire Tour S",
        "type": "Sedan",
        "price_range_inr": {
            "min_ex_showroom": 624000,
            "max_ex_showroom": 710000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1197, "cylinders": 3, "fuel_type": "Petrol"},
                {"displacement_cc": 1197, "cylinders": 3, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual"]
        },
        "fuel_tank": {"petrol_litres": 37, "cng_litres": 55},
        "dimensions": {
            "length_mm": 3995,
            "width_mm": 1735,
            "height_mm": 1520,
            "wheelbase_mm": 2450,
            "ground_clearance_mm": 163,
            "boot_space_litres": 378,
            "seating_capacity": 5,
            "doors": 4
        },
        "safety": {
            "airbags": 2,
            "abs": True,
            "ebd": True,
            "esc": False,
            "hill_assist": False,
            "isofix": False,
            "ncap_stars": None
        },
        "colours": [
            "Solid White",
            "Metallic Silky Silver",
            "Bluish Black"
        ],
        "user_rating": 4.5,
        "review_count": 52
    },
    {
        "make": "Maruti Suzuki",
        "model": "Eeco Cargo",
        "type": "Van",
        "price_range_inr": {
            "min_ex_showroom": 539000,
            "max_ex_showroom": 661000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1197, "cylinders": 4, "fuel_type": "Petrol"},
                {"displacement_cc": 1197, "cylinders": 4, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual"]
        },
        "fuel_tank": {"petrol_litres": 32, "cng_litres": 65},
        "dimensions": {
            "length_mm": 3675,
            "width_mm": 1475,
            "height_mm": 1825,
            "wheelbase_mm": 2350,
            "ground_clearance_mm": 160,
            "boot_space_litres": 660,
            "seating_capacity": 2,
            "doors": 5
        },
        "safety": {
            "airbags": 2,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": False,
            "isofix": False,
            "ncap_stars": 2
        },
        "colours": [
            "Solid White",
            "Metallic Silky Silver",
            "Metallic Brisk Blue"
        ],
        "user_rating": 4.3,
        "review_count": 13
    },
    {
        "make": "Maruti Suzuki",
        "model": "Eeco Tour V",
        "type": "MUV",
        "price_range_inr": {
            "min_ex_showroom": 518000,
            "max_ex_showroom": 633000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1197, "cylinders": 4, "fuel_type": "Petrol"},
                {"displacement_cc": 1197, "cylinders": 4, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual"]
        },
        "fuel_tank": {"petrol_litres": 32, "cng_litres": 65},
        "dimensions": {
            "length_mm": 3675,
            "width_mm": 1475,
            "height_mm": 1825,
            "wheelbase_mm": 2350,
            "ground_clearance_mm": 160,
            "boot_space_litres": 540,
            "seating_capacity": 6,
            "doors": 5
        },
        "safety": {
            "airbags": 2,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": False,
            "isofix": False,
            "ncap_stars": None
        },
        "colours": [
            "Solid White",
            "Metallic Silky Silver",
            "Bluish Black"
        ],
        "user_rating": 4.2,
        "review_count": 8
    },
    {
        "make": "Maruti Suzuki",
        "model": "Ertiga Tour",
        "type": "MUV",
        "price_range_inr": {
            "min_ex_showroom": 968000,
            "max_ex_showroom": 1059000
        },
        "engine": {
            "options": [
                {"displacement_cc": 1462, "cylinders": 4, "fuel_type": "Petrol"},
                {"displacement_cc": 1462, "cylinders": 4, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual"]
        },
        "fuel_tank": {"petrol_litres": 45, "cng_litres": 60},
        "dimensions": {
            "length_mm": 4395,
            "width_mm": 1735,
            "height_mm": 1690,
            "wheelbase_mm": 2670,
            "ground_clearance_mm": 185,
            "boot_space_litres": 209,
            "seating_capacity": 7,
            "doors": 5
        },
        "safety": {
            "airbags": 2,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": True,
            "isofix": True,
            "ncap_stars": None
        },
        "colours": [
            "Pearl Arctic White",
            "Splendid Silver",
            "Magma Grey"
        ],
        "user_rating": 4.4,
        "review_count": 57
    },
    {
        "make": "Maruti Suzuki",
        "model": "Wagon R Tour",
        "type": "Hatchback",
        "price_range_inr": {
            "min_ex_showroom": 499000,
            "max_ex_showroom": 589000
        },
        "engine": {
            "options": [
                {"displacement_cc": 998, "cylinders": 3, "fuel_type": "Petrol"},
                {"displacement_cc": 998, "cylinders": 3, "fuel_type": "CNG"}
            ],
            "transmissions": ["Manual"]
        },
        "fuel_tank": {"petrol_litres": 32, "cng_litres": 60},
        "dimensions": {
            "length_mm": 3655,
            "width_mm": 1620,
            "height_mm": 1675,
            "wheelbase_mm": 2435,
            "ground_clearance_mm": 165,
            "boot_space_litres": 341,
            "seating_capacity": 5,
            "doors": 5
        },
        "safety": {
            "airbags": 2,
            "abs": True,
            "ebd": True,
            "esc": True,
            "hill_assist": False,
            "isofix": False,
            "ncap_stars": None
        },
        "colours": [
            "Superior White",
            "Silky Silver",
            "Magma Grey"
        ],
        "user_rating": 4.2,
        "review_count": 71
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
        "price_ex_showroom_inr": 579000, "price_on_road_inr": 638383,
        "mileage": 24.8, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "ABS + EBD + ESC",
            "Keyless Entry", "Rear Parking Sensors",
            "Digital Cluster", "Halogen Projector Headlamps",
            "Driver Attention Warning"
        ]
    },
    {
        "car_model": "Swift", "name": "VXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 659000, "price_on_road_inr": 754778,
        "mileage": 24.8, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "7-inch Touchscreen",
            "Android Auto & Apple CarPlay (Wired)",
            "4-Speaker Audio System",
            "Steering Mounted Controls",
            "Power Windows", "Manual AC"
        ]
    },
    {
        "car_model": "Swift", "name": "VXi Opt",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 685000, "price_on_road_inr": 790731,
        "mileage": 24.8, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "Auto Climate Control",
            "7-inch Touchscreen",
            "Android Auto & Apple CarPlay (Wired)",
            "Steering Mounted Controls",
            "Rear Defogger", "Rear Wiper & Washer"
        ]
    },
    {
        "car_model": "Swift", "name": "VXi Automatic",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 704000, "price_on_road_inr": 813195,
        "mileage": 25.75, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "Automatic Gearbox",
            "7-inch Touchscreen",
            "Android Auto & Apple CarPlay (Wired)",
            "Auto Gear Shift", "Steering Mounted Controls"
        ]
    },
    {
        "car_model": "Swift", "name": "VXi Opt Automatic",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 730000, "price_on_road_inr": 830949,
        "mileage": 25.75, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "Automatic Gearbox",
            "Auto Climate Control",
            "7-inch Touchscreen",
            "Rear Wiper & Washer",
            "Rear Defogger"
        ]
    },
    {
        "car_model": "Swift", "name": "VXi CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 745000, "price_on_road_inr": 849814,
        "mileage": 32.85, "mileage_unit": "km/kg",
        "power_bhp": 68.80, "torque_nm": 101.8,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel",
            "7-inch Touchscreen",
            "Android Auto & Apple CarPlay (Wired)",
            "Manual AC", "Steering Mounted Controls"
        ]
    },
    {
        "car_model": "Swift", "name": "VXi Opt CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 771000, "price_on_road_inr": 875814,
        "mileage": 32.85, "mileage_unit": "km/kg",
        "power_bhp": 68.80, "torque_nm": 101.8,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel",
            "Auto Climate Control",
            "Rear Defogger", "Rear Wiper & Washer",
            "Steering Mounted Controls"
        ]
    },
    {
        "car_model": "Swift", "name": "ZXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 753000, "price_on_road_inr": 866986,
        "mileage": 24.8, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "LED Headlights", "LED DRLs",
            "15-inch Alloy Wheels",
            "Cruise Control", "Push Button Start",
            "Auto Climate Control",
            "Height Adjustable Driver Seat",
            "Rear Defogger", "Rear Wiper & Washer"
        ]
    },
    {
        "car_model": "Swift", "name": "ZXi Automatic",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 798000, "price_on_road_inr": 904475,
        "mileage": 25.75, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "Automatic Gearbox",
            "LED Headlights", "15-inch Alloy Wheels",
            "Cruise Control", "Push Button Start",
            "Auto Climate Control",
            "Rear Defogger", "Rear Wiper & Washer"
        ]
    },
    {
        "car_model": "Swift", "name": "ZXi CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 839000, "price_on_road_inr": 941236,
        "mileage": 32.85, "mileage_unit": "km/kg",
        "power_bhp": 68.80, "torque_nm": 101.8,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel",
            "LED Headlights", "15-inch Alloy Wheels",
            "Cruise Control", "Push Button Start",
            "Auto Climate Control"
        ]
    },
    {
        "car_model": "Swift", "name": "ZXi Plus",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 820000, "price_on_road_inr": 941236,
        "mileage": 24.8, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "9-inch SmartPlay Pro+ Touchscreen",
            "Wireless Android Auto & Apple CarPlay",
            "Wireless Phone Charging",
            "Rear Camera", "6-Speaker Audio System",
            "Connected Car Tech", "Geo-fence Alert",
            "Remote Door Lock/Unlock", "Vehicle Tracking"
        ]
    },
    {
        "car_model": "Swift", "name": "ZXi Plus DT",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 835000, "price_on_road_inr": 956991,
        "mileage": 24.8, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "9-inch SmartPlay Pro+ Touchscreen",
            "Dual-Tone Roof",
            "Wireless Android Auto & Apple CarPlay",
            "Rear Camera", "Connected Car Tech"
        ]
    },
    {
        "car_model": "Swift", "name": "ZXi Plus Automatic",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 865000, "price_on_road_inr": 996991,
        "mileage": 25.75, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "Automatic Gearbox",
            "9-inch SmartPlay Pro+ Touchscreen",
            "Wireless Android Auto & Apple CarPlay",
            "Rear Camera", "Connected Car Tech",
            "Wireless Phone Charging"
        ]
    },
    {
        "car_model": "Swift", "name": "ZXi Plus Automatic DT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 880000, "price_on_road_inr": 1012991,
        "mileage": 25.75, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "Automatic Gearbox",
            "9-inch SmartPlay Pro+ Touchscreen",
            "Dual-Tone Roof",
            "Wireless Android Auto & Apple CarPlay",
            "Rear Camera", "Connected Car Tech"
        ]
    },
    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  WAGON R  VARIANTS
    # ╚══════════════════════════════════════════════════════════════════════════
    {
        "car_model": "Wagon R", "name": "LXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 499000, "price_on_road_inr": 551470,
        "mileage": 24.35, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89.0,
        "key_features": [
            "6 Airbags", "ABS + EBD + ESC",
            "Rear Parking Sensors", "Idle Start-Stop",
            "Power Windows (Front)", "Halogen Headlamps"
        ]
    },
    {
        "car_model": "Wagon R", "name": "VXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 552000, "price_on_road_inr": 614386,
        "mileage": 24.35, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89.0,
        "key_features": [
            "6 Airbags", "Power Windows (Front + Rear)",
            "60:40 Split Rear Seat", "Keyless Entry",
            "Rear Parking Sensors", "Bluetooth/AUX Audio with 2 Speakers"
        ]
    },
    {
        "car_model": "Wagon R", "name": "LXi CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 589000, "price_on_road_inr": 661412,
        "mileage": 34.05, "mileage_unit": "km/kg",
        "power_bhp": 55.92, "torque_nm": 82.1,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel",
            "Rear Parking Sensors", "Power Windows (Front)",
            "Idle Start-Stop"
        ]
    },
    {
        "car_model": "Wagon R", "name": "ZXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 596000, "price_on_road_inr": 666820,
        "mileage": 23.56, "mileage_unit": "kmpl",
        "power_bhp": 88.50, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "1.2L 1197cc Engine", "Steering Mounted Controls",
            "Electrically Adjustable ORVMs", "Tilt Adjustable Steering",
            "60:40 Split Rear Seat", "Keyless Entry"
        ]
    },
    {
        "car_model": "Wagon R", "name": "VXi AMT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 597000, "price_on_road_inr": 662455,
        "mileage": 25.19, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89.0,
        "key_features": [
            "6 Airbags", "AMT Gearbox", "Hill Hold Assist",
            "Power Windows (Front + Rear)", "60:40 Split Rear Seat",
            "Keyless Entry", "Rear Parking Sensors"
        ]
    },
    {
        "car_model": "Wagon R", "name": "VXi CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 642000, "price_on_road_inr": 724300,
        "mileage": 34.05, "mileage_unit": "km/kg",
        "power_bhp": 55.92, "torque_nm": 82.1,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel",
            "Power Windows (Front + Rear)", "60:40 Split Rear Seat",
            "Keyless Entry", "Rear Parking Sensors"
        ]
    },
    {
        "car_model": "Wagon R", "name": "ZXi AMT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 641000, "price_on_road_inr": 733279,
        "mileage": 24.43, "mileage_unit": "kmpl",
        "power_bhp": 88.50, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "1.2L 1197cc Engine", "AMT Gearbox",
            "Hill Hold Assist", "Steering Mounted Controls",
            "Electrically Adjustable ORVMs", "Keyless Entry"
        ]
    },
    {
        "car_model": "Wagon R", "name": "ZXi Plus",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 639000, "price_on_road_inr": 731964,
        "mileage": 23.56, "mileage_unit": "kmpl",
        "power_bhp": 88.50, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "1.2L 1197cc Engine",
            "7-inch Touchscreen", "Android Auto & Apple CarPlay",
            "Front Fog Lamps", "14-inch Black Alloy Wheels",
            "4 Speakers", "ORVM Mounted Indicators"
        ]
    },
    {
        "car_model": "Wagon R", "name": "ZXi Plus AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 684000, "price_on_road_inr": 781431,
        "mileage": 24.43, "mileage_unit": "kmpl",
        "power_bhp": 88.50, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "1.2L 1197cc Engine", "AMT Gearbox",
            "7-inch Touchscreen", "Android Auto & Apple CarPlay",
            "Front Fog Lamps", "14-inch Black Alloy Wheels", "4 Speakers"
        ]
    },
    {
        "car_model": "Wagon R", "name": "ZXi Plus Dual Tone",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 650000, "price_on_road_inr": 743000,
        "mileage": 23.56, "mileage_unit": "kmpl",
        "power_bhp": 88.50, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "1.2L 1197cc Engine", "Dual-Tone Paint",
            "7-inch Touchscreen", "Android Auto & Apple CarPlay",
            "Front Fog Lamps", "14-inch Black Alloy Wheels", "4 Speakers"
        ]
    },
    {
        "car_model": "Wagon R", "name": "ZXi Plus AT Dual Tone",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 695000, "price_on_road_inr": 798300,
        "mileage": 24.43, "mileage_unit": "kmpl",
        "power_bhp": 88.50, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "1.2L 1197cc Engine", "AMT Gearbox",
            "Dual-Tone Paint", "7-inch Touchscreen",
            "Android Auto & Apple CarPlay",
            "Front Fog Lamps", "14-inch Black Alloy Wheels", "4 Speakers"
        ]
    },

    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  BALENO  VARIANTS
    # ╚══════════════════════════════════════════════════════════════════════════
    {
        "car_model": "Baleno", "name": "Sigma",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 599000, "price_on_road_inr": 666141,
        "mileage": 22.35, "mileage_unit": "kmpl",
        "power_bhp": 88.5, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "ABS + EBD", "Rear Parking Sensors",
            "Auto AC", "Halogen Projector Headlamps",
            "16-inch Steel Wheels", "4-Star Bharat NCAP"
        ]
    },
    {
        "car_model": "Baleno", "name": "Delta",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 680000, "price_on_road_inr": 755000,
        "mileage": 22.35, "mileage_unit": "kmpl",
        "power_bhp": 88.5, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "ABS + EBD + ESC", "Keyless Entry",
            "Steering Mounted Controls", "Rear Parking Sensors",
            "7-inch Touchscreen", "Wired Android Auto & Apple CarPlay"
        ]
    },
    {
        "car_model": "Baleno", "name": "Delta AMT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 730000, "price_on_road_inr": 810000,
        "mileage": 22.94, "mileage_unit": "kmpl",
        "power_bhp": 88.5, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "AMT Gearbox", "ABS + EBD + ESC",
            "Keyless Entry", "Steering Mounted Controls",
            "7-inch Touchscreen", "Wired Android Auto & Apple CarPlay"
        ]
    },
    {
        "car_model": "Baleno", "name": "Delta CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 770000, "price_on_road_inr": 855000,
        "mileage": 30.61, "mileage_unit": "km/kg",
        "power_bhp": 76.43, "torque_nm": 98.5,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel", "ABS + EBD + ESC",
            "Keyless Entry", "Steering Mounted Controls",
            "7-inch Touchscreen", "Wired Android Auto & Apple CarPlay"
        ]
    },
    {
        "car_model": "Baleno", "name": "Zeta",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 770000, "price_on_road_inr": 855000,
        "mileage": 22.35, "mileage_unit": "kmpl",
        "power_bhp": 88.5, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "Auto Climate Control", "Push Button Start",
            "7-inch Touchscreen", "Wireless Android Auto & Apple CarPlay",
            "Rear View Camera", "LED Headlamps", "Rear AC Vents"
        ]
    },
    {
        "car_model": "Baleno", "name": "Zeta AMT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 820000, "price_on_road_inr": 910000,
        "mileage": 22.94, "mileage_unit": "kmpl",
        "power_bhp": 88.5, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "AMT Gearbox", "Auto Climate Control",
            "7-inch Touchscreen", "Wireless Android Auto & Apple CarPlay",
            "Rear View Camera", "LED Headlamps", "Push Button Start"
        ]
    },
    {
        "car_model": "Baleno", "name": "Zeta CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 860000, "price_on_road_inr": 955000,
        "mileage": 30.61, "mileage_unit": "km/kg",
        "power_bhp": 76.43, "torque_nm": 98.5,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel", "Auto Climate Control",
            "7-inch Touchscreen", "Wireless Android Auto & Apple CarPlay",
            "Rear View Camera", "LED Headlamps", "Push Button Start"
        ]
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
            "16-inch Machined Alloy Wheels", "Tilt & Telescopic Steering"
        ]
    },
    {
        "car_model": "Baleno", "name": "Alpha AMT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 910000, "price_on_road_inr": 1010000,
        "mileage": 22.94, "mileage_unit": "kmpl",
        "power_bhp": 88.5, "torque_nm": 113.0,
        "key_features": [
            "6 Airbags", "AMT Gearbox", "Auto Climate Control",
            "9-inch Touchscreen", "Wireless Android Auto & Apple CarPlay",
            "Heads-Up Display", "360-Degree Camera", "Cruise Control",
            "16-inch Machined Alloy Wheels", "Tilt & Telescopic Steering"
        ]
    },
    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  BREZZA  VARIANTS
    # ╚══════════════════════════════════════════════════════════════════════════
    {
        "car_model": "Brezza", "name": "VXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 926000, "price_on_road_inr": 1040000,
        "mileage": 19.89, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 136.8,
        "key_features": [
            "6 Airbags", "Smart Hybrid Engine", "ABS + EBD + ESC",
            "Halogen Projector Headlamps", "Keyless Entry",
            "7-inch Touchscreen", "Android Auto & Apple CarPlay (Wired)",
            "4 Speakers", "Auto AC with Rear Vents"
        ]
    },
    {
        "car_model": "Brezza", "name": "ZXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1040000, "price_on_road_inr": 1165000,
        "mileage": 19.89, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 136.8,
        "key_features": [
            "6 Airbags", "Smart Hybrid Engine", "Auto Climate Control",
            "Push Button Start", "LED Headlamps with DRLs",
            "7-inch SmartPlay Pro Touchscreen", "Electric Sunroof",
            "Wireless Android Auto & Apple CarPlay", "Painted Alloy Wheels"
        ]
    },
    {
        "car_model": "Brezza", "name": "VXi AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1060000, "price_on_road_inr": 1190000,
        "mileage": 19.80, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 136.8,
        "key_features": [
            "6 Airbags", "Smart Hybrid Engine", "6-Speed Torque Converter",
            "ABS + EBD + ESC", "Paddle Shifters", "Keyless Entry",
            "Halogen Projector Headlamps", "7-inch Touchscreen",
            "Android Auto & Apple CarPlay (Wired)"
        ]
    },
    {
        "car_model": "Brezza", "name": "ZXi AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1175000, "price_on_road_inr": 1315000,
        "mileage": 19.80, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 136.8,
        "key_features": [
            "6 Airbags", "Smart Hybrid Engine", "6-Speed Torque Converter",
            "Auto Climate Control", "Push Button Start",
            "LED Headlamps with DRLs", "7-inch SmartPlay Pro Touchscreen",
            "Electric Sunroof", "Painted Alloy Wheels"
        ]
    },
    {
        "car_model": "Brezza", "name": "ZXi CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 1131000, "price_on_road_inr": 1270000,
        "mileage": 25.51, "mileage_unit": "km/kg",
        "power_bhp": 86.63, "torque_nm": 121.5,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel", "Electric Sunroof",
            "Auto Climate Control", "Push Button Start",
            "LED Headlamps with DRLs", "7-inch SmartPlay Pro Touchscreen",
            "Wireless Android Auto & Apple CarPlay", "Painted Alloy Wheels"
        ]
    },
    {
        "car_model": "Brezza", "name": "ZXi CNG DT",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 1146000, "price_on_road_inr": 1285000,
        "mileage": 25.51, "mileage_unit": "km/kg",
        "power_bhp": 86.63, "torque_nm": 121.5,
        "key_features": [
            "6 Airbags", "CNG + Petrol Bi-fuel", "Dual-Tone Exterior",
            "Auto Climate Control", "Push Button Start", "Electric Sunroof",
            "LED Headlamps with DRLs", "7-inch SmartPlay Pro Touchscreen",
            "Painted Alloy Wheels"
        ]
    },
    {
        "car_model": "Brezza", "name": "ZXi AT DT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1190000, "price_on_road_inr": 1330000,
        "mileage": 19.80, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 136.8,
        "key_features": [
            "6 Airbags", "Smart Hybrid Engine", "6-Speed Torque Converter",
            "Dual-Tone Exterior", "Auto Climate Control", "Push Button Start",
            "7-inch SmartPlay Pro Touchscreen", "Electric Sunroof", "Painted Alloy Wheels"
        ]
    },
    {
        "car_model": "Brezza", "name": "ZXi Plus",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1151000, "price_on_road_inr": 1290000,
        "mileage": 19.89, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 136.8,
        "key_features": [
            "6 Airbags", "Smart Hybrid Engine", "360-Degree Camera",
            "Heads-Up Display", "Electric Sunroof", "Precision Cut Alloy Wheels",
            "Auto Climate Control", "9-inch SmartPlay Pro+ Touchscreen",
            "Wireless Charging", "ARKAMYS Surround Sound", "LED Fog Lamps"
        ]
    },
    {
        "car_model": "Brezza", "name": "ZXi Plus DT",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1166000, "price_on_road_inr": 1305000,
        "mileage": 19.89, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 136.8,
        "key_features": [
            "6 Airbags", "Smart Hybrid Engine", "360-Degree Camera",
            "Heads-Up Display", "Electric Sunroof", "Dual-Tone Exterior",
            "Cooled Glove Box", "Precision Cut Alloy Wheels",
            "9-inch SmartPlay Pro+ Touchscreen", "Wireless Charging"
        ]
    },
    {
        "car_model": "Brezza", "name": "ZXi Plus AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1286000, "price_on_road_inr": 1440000,
        "mileage": 19.80, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 136.8,
        "key_features": [
            "6 Airbags", "Smart Hybrid Engine", "6-Speed Torque Converter",
            "360-Degree Camera", "Heads-Up Display", "Electric Sunroof",
            "Auto Climate Control", "Cooled Glove Box", "Precision Cut Alloys",
            "9-inch SmartPlay Pro+ Touchscreen", "Wireless Charging",
            "ARKAMYS Surround Sound"
        ]
    },
    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  JIMNY  VARIANTS
    # ╚══════════════════════════════════════════════════════════════════════════
    {
        "car_model": "Jimny", "name": "Zeta",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1231000, "price_on_road_inr": 1398517,
        "mileage": 16.94, "mileage_unit": "kmpl",
        "power_bhp": 103.0, "torque_nm": 134.2,
        "key_features": [
            "6 Airbags", "4WD AllGrip Pro", "Hill Assist",
            "Hill Descent Control", "ABS + EBD + ESC",
            "7-inch Touchscreen", "Wireless Android Auto & Apple CarPlay",
            "Keyless Entry", "Rear Parking Sensors"
        ]
    },
    {
        "car_model": "Jimny", "name": "Zeta AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1338000, "price_on_road_inr": 1525000,
        "mileage": 16.39, "mileage_unit": "kmpl",
        "power_bhp": 103.0, "torque_nm": 134.2,
        "key_features": [
            "6 Airbags", "4WD AllGrip Pro", "4-Speed AT Gearbox",
            "Hill Assist", "Hill Descent Control",
            "7-inch Touchscreen", "Wireless Android Auto & Apple CarPlay",
            "Keyless Entry", "Rear Parking Sensors"
        ]
    },
    {
        "car_model": "Jimny", "name": "Alpha",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1323000, "price_on_road_inr": 1515000,
        "mileage": 16.94, "mileage_unit": "kmpl",
        "power_bhp": 103.0, "torque_nm": 134.2,
        "key_features": [
            "6 Airbags", "4WD AllGrip Pro", "Hill Assist",
            "Hill Descent Control", "Auto Climate Control",
            "Cruise Control", "LED Projector Headlamps", "Headlamp Washers",
            "9-inch SmartPlay Pro+ Touchscreen", "Alloy Wheels",
            "Rear Camera", "Analogue Cluster with MID", "Push Button Start"
        ]
    },
    {
        "car_model": "Jimny", "name": "Alpha Dual Tone",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1339000, "price_on_road_inr": 1535000,
        "mileage": 16.94, "mileage_unit": "kmpl",
        "power_bhp": 103.0, "torque_nm": 134.2,
        "key_features": [
            "6 Airbags", "4WD AllGrip Pro", "Dual-Tone Roof",
            "Hill Assist", "Hill Descent Control", "Auto Climate Control",
            "Cruise Control", "LED Projector Headlamps", "Headlamp Washers",
            "9-inch SmartPlay Pro+ Touchscreen", "Alloy Wheels", 
            "Rear Camera", "Analogue Cluster with MID", "Push Button Start"
        ]
    },
    {
        "car_model": "Jimny", "name": "Alpha AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1429000, "price_on_road_inr": 1635000,
        "mileage": 16.39, "mileage_unit": "kmpl",
        "power_bhp": 103.0, "torque_nm": 134.2,
        "key_features": [
            "6 Airbags", "4WD AllGrip Pro", "4-Speed AT Gearbox",
            "Hill Assist", "Hill Descent Control", "Auto Climate Control",
            "Cruise Control", "LED Projector Headlamps", "Headlamp Washers",
            "9-inch SmartPlay Pro+ Touchscreen", "Alloy Wheels",
            "Rear Camera", "Analogue Cluster with MID", "Push Button Start"
        ]
    },
    {
        "car_model": "Jimny", "name": "Alpha Dual Tone AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1445000, "price_on_road_inr": 1655000,
        "mileage": 16.39, "mileage_unit": "kmpl",
        "power_bhp": 103.0, "torque_nm": 134.2,
        "key_features": [
            "6 Airbags", "4WD AllGrip Pro", "4-Speed AT Gearbox",
            "Dual-Tone Roof", "Hill Assist", "Hill Descent Control",
            "Auto Climate Control", "Cruise Control",
            "LED Projector Headlamps", "Headlamp Washers",
            "9-inch SmartPlay Pro+ Touchscreen", "Alloy Wheels",
            "Rear Camera", "Analogue Cluster with MID", "Push Button Start"
        ]
    },
    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  Ertiga  VARIANTS
    # ╚══════════════════════════════════════════════════════════════════════════

    {
    "car_model": "Ertiga", "name": "LXi",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 880000, "price_on_road_inr": 984829,
    "mileage": 20.51, "mileage_unit": "kmpl",
    "power_bhp": 101.64, "torque_nm": 136.8,
    "key_features": [
        "6 Airbags (Standard)", "ABS + EBD", "ESP with Hill Hold",
        "Projector Halogen Headlamps", "Power Windows (Front & Rear)",
    ],
},
{
    "car_model": "Ertiga", "name": "VXi",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 985000, "price_on_road_inr": 1135000,
    "mileage": 20.51, "mileage_unit": "kmpl",
    "power_bhp": 101.64, "torque_nm": 136.8,
    "key_features": [
        "6 Airbags", "Keyless Entry", "Steering Mounted Controls",
        "Body Coloured ORVMs with Turn Indicators", "4-Speaker Audio System",
    ],
},
{
    "car_model": "Ertiga", "name": "VXi AT",
    "fuel": "Petrol", "transmission": "Automatic",
    "price_ex_showroom_inr": 1120000, "price_on_road_inr": 1315000,
    "mileage": 20.30, "mileage_unit": "kmpl",
    "power_bhp": 101.64, "torque_nm": 136.8,
    "key_features": [
        "6-Speed Torque Converter", "Paddle Shifters",
        "ESP with Hill Hold", "6 Airbags",
    ],
},
{
    "car_model": "Ertiga", "name": "VXi CNG",
    "fuel": "CNG", "transmission": "Manual",
    "price_ex_showroom_inr": 1076000, "price_on_road_inr": 1210000,
    "mileage": 26.11, "mileage_unit": "km/kg",
    "power_bhp": 86.63, "torque_nm": 121.5,
    "key_features": [
        "6 Airbags", "S-CNG Dual ECU Technology",
        "Keyless Entry", "Steering Mounted Audio Controls",
    ],
},
{
    "car_model": "Ertiga", "name": "ZXi",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 1091000, "price_on_road_inr": 1255000,
    "mileage": 20.51, "mileage_unit": "kmpl",
    "power_bhp": 101.64, "torque_nm": 136.8,
    "key_features": [
        "6 Airbags", "Auto Climate Control", "7-inch SmartPlay Studio",
        "Push Button Start", "15-inch Alloy Wheels",
    ],
},
{
    "car_model": "Ertiga", "name": "ZXi AT",
    "fuel": "Petrol", "transmission": "Automatic",
    "price_ex_showroom_inr": 1227000, "price_on_road_inr": 1410000,
    "mileage": 20.30, "mileage_unit": "kmpl",
    "power_bhp": 101.64, "torque_nm": 136.8,
    "key_features": [
        "6-Speed AT with Paddle Shifters", "6 Airbags",
        "Cruise Control", "7-inch Touchscreen",
    ],
},
{
    "car_model": "Ertiga", "name": "ZXi CNG",
    "fuel": "CNG", "transmission": "Manual",
    "price_ex_showroom_inr": 1182000, "price_on_road_inr": 1335000,
    "mileage": 26.11, "mileage_unit": "km/kg",
    "power_bhp": 86.63, "torque_nm": 121.5,
    "key_features": [
        "6 Airbags", "Alloy Wheels",
        "Auto Climate Control", "7-inch SmartPlay Studio",
    ],
},
{
    "car_model": "Ertiga", "name": "ZXi Plus",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 1159000, "price_on_road_inr": 1345000,
    "mileage": 20.51, "mileage_unit": "kmpl",
    "power_bhp": 101.64, "torque_nm": 136.8,
    "key_features": [
        "6 Airbags", "Rear Parking Camera", "Cruise Control",
        "Wireless Android Auto/Apple CarPlay", "Arkamys Sound System",
    ],
},
{
    "car_model": "Ertiga", "name": "ZXi Plus AT",
    "fuel": "Petrol", "transmission": "Automatic",
    "price_ex_showroom_inr": 1294000, "price_on_road_inr": 1505000,
    "mileage": 20.30, "mileage_unit": "kmpl",
    "power_bhp": 101.64, "torque_nm": 136.8,
    "key_features": [
        "6 Airbags", "6-Speed AT with Paddle Shifters",
        "Rear Parking Camera", "Auto Headlamps",
        "SmartPlay Pro Touchscreen",
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
    "price_on_road_inr": 1364000,
    "mileage": 20.97,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "6 Airbags (Standard)", "Cruise Control", "7-inch Touchscreen",
      "Full LED Headlamps", "16-inch Alloy Wheels"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Zeta CNG",
    "fuel": "CNG",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1243000,
    "price_on_road_inr": 1421000,
    "mileage": 26.32,
    "mileage_unit": "km/kg",
    "power_bhp": 86.63,
    "torque_nm": 121.5,
    "key_features": [
      "Dual Fuel (S-CNG)", "6 Airbags",
      " Steering Mounted Controls", "7-inch SmartPlay Studio"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Alpha",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1249000,
    "price_on_road_inr": 1477000,
    "mileage": 20.97,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "360 Degree Camera", "Leatherette Upholstery",
      "Auto Headlamps", "UV Cut Glass", "6 Airbags"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Zeta AT",
    "fuel": "Petrol",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1287000,
    "price_on_road_inr": 1535000,
    "mileage": 20.27,
    "mileage_unit": "kmpl",
    "power_bhp": 99.0,
    "torque_nm": 136.0,
    "key_features": [
      "6-Speed Torque Converter", "Paddle Shifters",
      "ESP with Hill Hold", "6 Airbags"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Alpha AT",
    "fuel": "Petrol",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1384000,
    "price_on_road_inr": 1635000,
    "mileage": 20.27,
    "mileage_unit": "kmpl",
    "power_bhp": 99.0,
    "torque_nm": 136.0,
    "key_features": [
      "6-Speed AT with Paddle Shifters", "360 Degree Camera",
      "Leatherette Seats", "6 Airbags"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Alpha Plus",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1297000,
    "price_on_road_inr": 1530000,
    "mileage": 20.97,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "Ventilated Front Seats", "TPMS (Highline)",
      "Premium Leatherette Seats", "6 Airbags"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Alpha Plus Dual Tone",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1312000,
    "price_on_road_inr": 1550000,
    "mileage": 20.97,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "Dual Tone Exterior", "Ventilated Seats",
      "TPMS", "Glossy Black Alloys", "6 Airbags"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Alpha Plus AT",
    "fuel": "Petrol",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1432000,
    "price_on_road_inr": 1691000,
    "mileage": 20.27,
    "mileage_unit": "kmpl",
    "power_bhp": 99.0,
    "torque_nm": 136.0,
    "key_features": [
      "Ventilated Seats", "6-Speed AT",
      "360 Degree Camera", "TPMS", "6 Airbags"
    ]
  },
  {
    "car_model": "XL6",
    "name": "Alpha Plus AT Dual Tone",
    "fuel": "Petrol",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1447000,
    "price_on_road_inr": 1710000,
    "mileage": 20.27,
    "mileage_unit": "kmpl",
    "power_bhp": 99.0,
    "torque_nm": 136.0,
    "key_features": [
      "Top Model", "Dual Tone Paint",
      "Ventilated Seats", "360 Degree Camera", "6 Airbags"
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
    "price_on_road_inr": 1216328,
    "mileage": 21.11,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "Halogen Projector Headlamps",
      "LED DRLs",
      "Keyless Entry with Push Button Start",
      "Auto AC with Rear Vents",
      "6 Airbags (Standard)",
      "ESP & Hill Hold Assist"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Delta",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1210000,
    "price_on_road_inr": 1385000,
    "mileage": 21.11,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "7-inch SmartPlay Studio",
      "Suzuki Connect",
      "Rear Parking Camera",
      "Cruise Control",
      "Steering Mounted Controls",
      "Paddle Shifters (AT only)"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Delta AT",
    "fuel": "Petrol",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1345000,
    "price_on_road_inr": 1545000,
    "mileage": 20.58,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "6-Speed Torque Converter",
      "Paddle Shifters",
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
    "price_on_road_inr": 1475000,
    "mileage": 26.6,
    "mileage_unit": "km/kg",
    "power_bhp": 86.63,
    "torque_nm": 121.5,
    "key_features": [
      "Factory-fit S-CNG Kit",
      "7-inch Touchscreen",
      "Cruise Control",
      "Steering Mounted Controls"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Zeta",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1370000,
    "price_on_road_inr": 1585000,
    "mileage": 21.11,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "Auto LED Headlamps",
      "17-inch Machined Alloys",
      "9-inch SmartPlay Pro+",
      "6-speaker Clarion Audio",
      "Ventilated Front Seats",
      "Panoramic Sunroof (Zeta Optional)"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Zeta CNG",
    "fuel": "CNG",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1460000,
    "price_on_road_inr": 1650000,
    "mileage": 26.6,
    "mileage_unit": "km/kg",
    "power_bhp": 86.63,
    "torque_nm": 121.5,
    "key_features": [
      "S-CNG Dual ECU",
      "LED Headlamps",
      "9-inch Touchscreen",
      "Auto-dimming IRVM"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Zeta Plus Hybrid CVT",
    "fuel": "Hybrid",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1792000,
    "price_on_road_inr": 2045000,
    "mileage": 27.97,
    "mileage_unit": "kmpl",
    "power_bhp": 115.5,
    "torque_nm": 141.0,
    "key_features": [
      "Self-Charging Strong Hybrid",
      "7-inch Digital Instrument Cluster",
      "Wireless Phone Charger",
      "Head-up Display",
      "Panoramic Sunroof"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Alpha",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 1520000,
    "price_on_road_inr": 1755000,
    "mileage": 21.11,
    "mileage_unit": "kmpl",
    "power_bhp": 101.64,
    "torque_nm": 136.8,
    "key_features": [
      "360-degree View Camera",
      "Leatherette Seats",
      "8-way Powered Driver Seat",
      "Soft-touch Dashboard",
      "AllGrip AWD (Optional)"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Alpha Plus Hybrid CVT",
    "fuel": "Hybrid",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1950000,
    "price_on_road_inr": 2245000,
    "mileage": 27.97,
    "mileage_unit": "kmpl",
    "power_bhp": 115.5,
    "torque_nm": 141.0,
    "key_features": [
      "Strong Hybrid System",
      "Ventilated Seats",
      "360-degree Camera",
      "Puddle Lamps",
      "Premium Leatherette Interiors"
    ]
  },
  {
    "car_model": "Grand Vitara",
    "name": "Alpha Plus Opt Hybrid CVT DT",
    "fuel": "Hybrid",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1972000,
    "price_on_road_inr": 2275000,
    "mileage": 27.97,
    "mileage_unit": "kmpl",
    "power_bhp": 115.5,
    "torque_nm": 141.0,
    "key_features": [
      "Dual Tone Exterior",
      "Panoramic Sunroof",
      "Premium Sound System",
      "TPMS (Highline)",
      "Strong Hybrid"
    ]
  },

    # Ignis variants
  {
    "car_model": "Ignis", "name": "Sigma",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 535100, "price_on_road_inr": 597000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "6 Airbags (Standard)", "ABS + EBD",
        "ISOFIX Child Seat Mounts", "Front Power Windows"
    ]
  },
  {
    "car_model": "Ignis", "name": "Delta",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 584500, "price_on_road_inr": 651000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "Audio System with Bluetooth", "Steering Mounted Controls",
        "Electrically Adjustable ORVMs", "Rear Power Windows"
    ]
  },
  {
    "car_model": "Ignis", "name": "Delta AMT",
    "fuel": "Petrol", "transmission": "Automatic",
    "price_ex_showroom_inr": 629500, "price_on_road_inr": 709000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "AMT Gearbox", "ESP with Hill Hold",
        "Dual Tone Dashboard", "Security Alarm"
    ]
  },
  {
    "car_model": "Ignis", "name": "Zeta",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 637500, "price_on_road_inr": 727000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "15-inch Alloy Wheels", "7-inch SmartPlay Studio",
        "Push Button Start/Stop", "Fog Lamps"
    ]
  },
  {
    "car_model": "Ignis", "name": "Zeta AMT",
    "fuel": "Petrol", "transmission": "Automatic",
    "price_ex_showroom_inr": 682500, "price_on_road_inr": 777000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "AMT Gearbox", "Alloy Wheels",
        "7-inch Touchscreen", "ESP with Hill Hold"
    ]
  },
  {
    "car_model": "Ignis", "name": "Alpha",
    "fuel": "Petrol", "transmission": "Manual",
    "price_ex_showroom_inr": 697000, "price_on_road_inr": 793000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "LED Projector Headlamps", "Automatic Climate Control",
        "Rearview Camera", "Height Adjustable Driver Seat"
    ]
  },
  {
    "car_model": "Ignis", "name": "Alpha AMT",
    "fuel": "Petrol", "transmission": "Automatic",
    "price_ex_showroom_inr": 742000, "price_on_road_inr": 843000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "AMT Gearbox", "Auto Climate Control",
        "Puddle Lamps", "SmartPlay Pro Touchscreen"
    ]
  },
  {
    "car_model": "Ignis", "name": "Alpha Dual Tone AMT",
    "fuel": "Petrol", "transmission": "Automatic",
    "price_ex_showroom_inr": 754700, "price_on_road_inr": 857000,
    "mileage": 20.89, "mileage_unit": "kmpl",
    "power_bhp": 81.8, "torque_nm": 113,
    "key_features": [
        "Dual Tone Roof Options", "LED DRLs",
        "Automatic Climate Control", "Rear Parking Camera"
    ]
  },
  {
    "car_model": "Ignis", 
    "name": "Delta Dual Tone AMT",
    "fuel": "Petrol", 
    "transmission": "Automatic",
    "price_ex_showroom_inr": 629500, 
    "price_on_road_inr": 709000,
    "mileage": 20.89, 
    "mileage_unit": "kmpl",
    "power_bhp": 81.8, 
    "torque_nm": 113,
    "key_features": [
        "Dual Tone Exterior Color", 
        "Steering Mounted Audio Controls",
        "Remote Keyless Entry", 
        "Electronic Stability Program (ESP)"
    ]
},

    #Ciaz variants
  {
    "car_model": "Ciaz",
    "name": "Sigma MT",
    "fuel": "Petrol",
    "transmission": "Manual",
    "price_ex_showroom_inr": 909000,
    "price_on_road_inr": 1012803,
    "mileage": 20.65,
    "mileage_unit": "kmpl",
    "power_bhp": 103.25,
    "torque_nm": 138,
    "key_features": [
      "2 Airbags",
      "ABS with EBD & ISOFIX",
      "Manual AC with Rear Vents",
      "Front & Rear Power Windows"
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
      "Cruise Control",
      "Automatic Climate Control",
      "15-inch Alloy Wheels",
      "Steering Mounted Controls"
    ]
  },
  {
    "car_model": "Ciaz",
    "name": "Delta AT",
    "fuel": "Petrol",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1073000,
    "price_on_road_inr": 1215000,
    "mileage": 20.04,
    "mileage_unit": "kmpl",
    "power_bhp": 103.25,
    "torque_nm": 138,
    "key_features": [
      "4-Speed Torque Converter",
      "ESP with Hill Hold",
      "Cruise Control",
      "Automatic Climate Control"
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
      "Push Button Start/Stop",
      "Rear Sunshade"
    ]
  },
  {
    "car_model": "Ciaz",
    "name": "Zeta AT",
    "fuel": "Petrol",
    "transmission": "Automatic",
    "price_ex_showroom_inr": 1112000,
    "price_on_road_inr": 1255000,
    "mileage": 20.04,
    "mileage_unit": "kmpl",
    "power_bhp": 103.25,
    "torque_nm": 138,
    "key_features": [
      "Automatic Transmission",
      "LED Projector Headlamps",
      "Reverse Parking Camera",
      "7-inch SmartPlay Studio"
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
      "Leatherette Seats",
      "16-inch Precision Cut Alloys",
      "SmartPlay Pro Touchscreen",
      "Auto Headlamps"
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
      "Top-End Automatic",
      "Leatherette Seats",
      "LED Fog Lamps",
      "Voice Command System"
    ]
  },
  #Alto K10 Variants
    {
        "car_model": "Alto K10", "name": "STD",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 370000, "price_on_road_inr": 415467,
        "mileage": 24.39, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89,
        "key_features": [
            "6 Airbags", "ABS + EBD",
            "Rear Parking Sensors", "ESP"
        ]
    },
    {
        "car_model": "Alto K10", "name": "LXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 400000, "price_on_road_inr": 453000,
        "mileage": 24.39, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89,
        "key_features": [
            "6 Airbags", "Power Steering", "AC"
        ]
    },
    {
        "car_model": "Alto K10", "name": "VXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 450000, "price_on_road_inr": 509000,
        "mileage": 24.39, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89,
        "key_features": [
            "6 Airbags", "Front Power Windows",
            "Bluetooth Audio", "2 Speakers"
        ]
    },
    {
        "car_model": "Alto K10", "name": "VXi Plus",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 500000, "price_on_road_inr": 562000,
        "mileage": 24.39, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89,
        "key_features": [
            "6 Airbags", "Touchscreen Infotainment",
            "Android Auto & Apple CarPlay",
            "4 Speakers", "Keyless Entry"
        ]
    },
    {
        "car_model": "Alto K10", "name": "VXi AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 495000, "price_on_road_inr": 560000,
        "mileage": 24.90, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89,
        "key_features": [
            "6 Airbags", "AMT Gearbox", "Hill Assist",
            "Bluetooth Audio", "Front Power Windows"
        ]
    },
    {
        "car_model": "Alto K10", "name": "VXi Plus AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 545000, "price_on_road_inr": 655000,
        "mileage": 24.90, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89,
        "key_features": [
            "6 Airbags", "AMT Gearbox", "SmartPlay Studio",
            "Android Auto & Apple CarPlay",
            "4 Speakers", "Keyless Entry"
        ]
    },
    {
        "car_model": "Alto K10", "name": "LXi CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 482000, "price_on_road_inr": 545000,
        "mileage": 33.85, "mileage_unit": "km/kg",
        "power_bhp": 55.92, "torque_nm": 82.1,
        "key_features": [
            "CNG + Petrol Bi-fuel",
            "6 Airbags", "ABS + EBD", "Power Steering"
        ]
    },
    {
        "car_model": "Alto K10", "name": "VXi CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 568000, "price_on_road_inr": 635000,
        "mileage": 33.85, "mileage_unit": "km/kg",
        "power_bhp": 55.92, "torque_nm": 82.1,
        "key_features": [
            "CNG + Petrol Bi-fuel", "6 Airbags",
            "Front Power Windows", "Bluetooth Audio"
        ]
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
      "6 Airbags",
      "ABS with EBD",
      "Reverse Parking Sensors",
      "Speed Limiting System",
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
      "6 Airbags",
      "Factory-Fitted S-CNG Kit",
      "Economical Running Costs",
      "Compact Size for Easy Parking",
      "Standard Safety Suite (ABS/EBD)"
    ]
  },

  # Celerio variants
    {
        "car_model": "Celerio", "name": "LXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 470000, "price_on_road_inr": 524963,
        "mileage": 25.24, "mileage_unit": "kmpl",
        "power_bhp": 67.77, "torque_nm": 91.1,
        "key_features": [
            "6 Airbags", "ABS + EBD",
            "Manual AC", "ESP"
        ]
    },
    {
        "car_model": "Celerio", "name": "VXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 516000, "price_on_road_inr": 580000,
        "mileage": 25.24, "mileage_unit": "kmpl",
        "power_bhp": 67.77, "torque_nm": 91.1,
        "key_features": [
            "6 Airbags", "Central Locking",
            "Front & Rear Power Windows", "Electric ORVMs"
        ]
    },
    {
        "car_model": "Celerio", "name": "VXi AMT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 561000, "price_on_road_inr": 630000,
        "mileage": 26.68, "mileage_unit": "kmpl",
        "power_bhp": 67.77, "torque_nm": 91.1,
        "key_features": [
            "6 Airbags", "AMT Gearbox", 
            "Hill Hold Assist", "Power Windows"
        ]
    },
    {
        "car_model": "Celerio", "name": "ZXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 571000, "price_on_road_inr": 640000,
        "mileage": 25.24, "mileage_unit": "kmpl",
        "power_bhp": 67.77, "torque_nm": 91.1,
        "key_features": [
            "6 Airbags", "Basic Audio System + Bluetooth",
            "Steering Mounted Controls", "Rear Defogger & Wiper"
        ]
    },
    {
        "car_model": "Celerio", "name": "VXi CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 598000, "price_on_road_inr": 670000,
        "mileage": 34.43, "mileage_unit": "km/kg",
        "power_bhp": 55.92, "torque_nm": 82.1,
        "key_features": [
            "CNG + Petrol Bi-fuel", "6 Airbags",
            "Central Locking", "Power Windows"
        ]
    },
    {
        "car_model": "Celerio", "name": "ZXi AMT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 616000, "price_on_road_inr": 690000,
        "mileage": 26.00, "mileage_unit": "kmpl",
        "power_bhp": 67.77, "torque_nm": 91.1,
        "key_features": [
            "6 Airbags", "AMT Gearbox", "Hill Hold Assist",
            "Steering Controls", "Basic Audio System"
        ]
    },
    {
        "car_model": "Celerio", "name": "ZXi Plus",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 628000, "price_on_road_inr": 700000,
        "mileage": 24.97, "mileage_unit": "kmpl",
        "power_bhp": 67.77, "torque_nm": 91.1,
        "key_features": [
            "6 Airbags", "7-inch Touchscreen Infotainment",
            "Push Button Start", "15-inch Alloy Wheels"
        ]
    },
    {
        "car_model": "Celerio", "name": "ZXi Plus AMT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 673000, "price_on_road_inr": 750000,
        "mileage": 26.00, "mileage_unit": "kmpl",
        "power_bhp": 67.77, "torque_nm": 91.1,
        "key_features": [
            "6 Airbags", "AMT Gearbox", "Hill Hold Assist",
            "7-inch Touchscreen", "Push Button Start"
        ]
    },

# Spresso Variants
    {
        "car_model": "S-Presso", "name": "STD",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 350000, "price_on_road_inr": 394457,
        "mileage": 24.12, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89,
        "key_features": [
            "Dual Front Airbags", "ABS + EBD",
            "ESP with Hill Hold (Optional)", "Digital Instrument Cluster"
        ]
    },
    {
        "car_model": "S-Presso", "name": "LXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 380000, "price_on_road_inr": 430000,
        "mileage": 24.12, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89,
        "key_features": [
            "Manual AC with Heater", "Power Steering",
            "Dual Front Airbags", "ABS + EBD"
        ]
    },
    {
        "car_model": "S-Presso", "name": "VXi",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 430000, "price_on_road_inr": 480000,
        "mileage": 24.76, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89,
        "key_features": [
            "Remote Keyless Entry", "Front Power Windows",
            "SmartPlay Dock (Bluetooth/USB/AUX)", "Body Coloured Bumpers"
        ]
    },
    {
        "car_model": "S-Presso", "name": "LXi CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 462000, "price_on_road_inr": 520000,
        "mileage": 32.73, "mileage_unit": "km/kg",
        "power_bhp": 55.92, "torque_nm": 82.1,
        "key_features": [
            "Factory-Fitted S-CNG Kit", "Manual AC with Heater",
            "Power Steering", "Dual Front Airbags"
        ]
    },
    {
        "car_model": "S-Presso", "name": "VXi Opt AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 475000, "price_on_road_inr": 535000,
        "mileage": 25.30, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89,
        "key_features": [
            "AMT Gearbox", "ESP with Hill Hold",
            "Front Power Windows", "Remote Keyless Entry"
        ]
    },
    {
        "car_model": "S-Presso", "name": "VXi Plus",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 480000, "price_on_road_inr": 540000,
        "mileage": 24.76, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89,
        "key_features": [
            "7-inch SmartPlay Studio Touchscreen", "Android Auto & Apple CarPlay",
            "Steering Mounted Controls", "Internally Adjustable ORVMs"
        ]
    },
    {
        "car_model": "S-Presso", "name": "VXi CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 512000, "price_on_road_inr": 575000,
        "mileage": 32.73, "mileage_unit": "km/kg",
        "power_bhp": 55.92, "torque_nm": 82.1,
        "key_features": [
            "Factory-Fitted S-CNG Kit", "Remote Keyless Entry",
            "Front Power Windows", "SmartPlay Dock"
        ]
    },
    {
        "car_model": "S-Presso", "name": "VXi Plus Opt AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 525000, "price_on_road_inr": 590000,
        "mileage": 25.30, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89,
        "key_features": [
            "7-inch Touchscreen", "Steering Mounted Controls",
            "Hill Hold Assist", "Body Coloured ORVMs & Door Handles"
        ]
    },

# Eeco Variants
    {
        "car_model": "Eeco", "name": "5 Seater STD",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 521000, "price_on_road_inr": 588426,
        "mileage": 19.71, "mileage_unit": "kmpl",
        "power_bhp": 79.65, "torque_nm": 105.5,
        "key_features": [
            "6 Airbags (Standard)", "ABS + EBD",
            "Rear Parking Sensors", "ESP", "Digital Instrument Cluster"
        ]
    },
    {
        "car_model": "Eeco", "name": "6 Seater STD",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 547000, "price_on_road_inr": 615000,
        "mileage": 19.71, "mileage_unit": "kmpl",
        "power_bhp": 79.65, "torque_nm": 105.5,
        "key_features": [
            "6 Seater Layout", "6 Airbags",
            "ABS + EBD", "3-point Seatbelts for all"
        ]
    },
    {
        "car_model": "Eeco", "name": "5 Seater AC",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 554000, "price_on_road_inr": 625000,
        "mileage": 19.71, "mileage_unit": "kmpl",
        "power_bhp": 79.65, "torque_nm": 105.5,
        "key_features": [
            "Manual AC", "Cabin Air Filter",
            "6 Airbags", "ABS + EBD", "ESP"
        ]
    },
    {
        "car_model": "Eeco", "name": "5 Seater AC CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 636000, "price_on_road_inr": 718000,
        "mileage": 26.78, "mileage_unit": "km/kg",
        "power_bhp": 70.67, "torque_nm": 95,
        "key_features": [
            "Factory-Fitted S-CNG Kit",
            "Manual AC", "6 Airbags",
            "ABS + EBD", "ESP"
        ]
    },

# Fronx Variants
    {
        "car_model": "Fronx", "name": "Sigma",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 685000, "price_on_road_inr": 779556,
        "mileage": 21.79, "mileage_unit": "kmpl",
        "power_bhp": 89, "torque_nm": 113,
        "key_features": [
            "6 Airbags (Standard)", "ABS + EBD",
            "Automatic AC", "Keyless Entry", "Power Windows"
        ]
    },
    {
        "car_model": "Fronx", "name": "Delta",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 765000, "price_on_road_inr": 868000,
        "mileage": 21.79, "mileage_unit": "kmpl",
        "power_bhp": 89, "torque_nm": 113,
        "key_features": [
            "6 Airbags", "7-inch Touchscreen",
            "Wireless Android Auto & Apple CarPlay", "Steering Controls"
        ]
    },
    {
        "car_model": "Fronx", "name": "Sigma CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 779000, "price_on_road_inr": 882000,
        "mileage": 28.51, "mileage_unit": "km/kg",
        "power_bhp": 76.43, "torque_nm": 98.5,
        "key_features": [
            "Factory-Fitted S-CNG", "6 Airbags",
            "Automatic AC", "ABS + EBD"
        ]
    },
    {
        "car_model": "Fronx", "name": "Delta AMT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 815000, "price_on_road_inr": 925000,
        "mileage": 22.89, "mileage_unit": "kmpl",
        "power_bhp": 89, "torque_nm": 113,
        "key_features": [
            "6 Airbags", "AMT Gearbox", "Hill Assist",
            "7-inch Touchscreen", "Steering Controls"
        ]
    },
    {
        "car_model": "Fronx", "name": "Delta Plus",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 804000, "price_on_road_inr": 912000,
        "mileage": 21.79, "mileage_unit": "kmpl",
        "power_bhp": 89, "torque_nm": 113,
        "key_features": [
            "6 Airbags", "LED Headlamps", 
            "16-inch Black Alloy Wheels", "LED DRLs"
        ]
    },
    {
        "car_model": "Fronx", "name": "Delta Plus Turbo",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 892000, "price_on_road_inr": 1012000,
        "mileage": 21.50, "mileage_unit": "kmpl",
        "power_bhp": 98.69, "torque_nm": 147.6,
        "key_features": [
            "1.0L BoosterJet Turbo Engine", "6 Airbags",
            "LED Headlamps", "16-inch Alloys"
        ]
    },
    {
        "car_model": "Fronx", "name": "Zeta Turbo",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 971000, "price_on_road_inr": 1105000,
        "mileage": 21.50, "mileage_unit": "kmpl",
        "power_bhp": 98.69, "torque_nm": 147.6,
        "key_features": [
            "Rear View Camera", "Push Button Start",
            "Wireless Phone Charger", "6 Airbags"
        ]
    },
    {
        "car_model": "Fronx", "name": "Alpha Turbo",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1056000, "price_on_road_inr": 1205000,
        "mileage": 21.50, "mileage_unit": "kmpl",
        "power_bhp": 98.69, "torque_nm": 147.6,
        "key_features": [
            "360 View Camera", "Heads-Up Display",
            "Cruise Control", "9-inch SmartPlay Pro+ Touchscreen"
        ]
    },
    {
        "car_model": "Fronx", "name": "Alpha Turbo AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1184000, "price_on_road_inr": 1355000,
        "mileage": 20.01, "mileage_unit": "kmpl",
        "power_bhp": 98.69, "torque_nm": 147.6,
        "key_features": [
            "6-Speed Torque Converter AT", "Paddle Shifters",
            "360 Camera", "Heads-Up Display"
        ]
    },
    {
    "car_model": "Fronx", "name": "Delta CNG",
    "fuel": "CNG", "transmission": "Manual",
    "price_ex_showroom_inr": 859000, "price_on_road_inr": 1007000,
    "mileage": 28.51, "mileage_unit": "km/kg",
    "power_bhp": 76.4, "torque_nm": 98.5,
    "key_features": [
        "7-inch Touchscreen Infotainment", "Wireless Android Auto/Apple CarPlay",
        "Steering Mounted Controls", "Automatic Climate Control", "6 Airbags"
    ]
},
{
    "car_model": "Fronx", "name": "Delta Plus AMT",
    "fuel": "Petrol", "transmission": "Automatic",
    "price_ex_showroom_inr": 855000, "price_on_road_inr": 975552,
    "mileage": 22.89, "mileage_unit": "kmpl",
    "power_bhp": 88.5, "torque_nm": 113,
    "key_features": [
        "LED Multi-Reflector Headlamps", "LED DRLs",
        "16-inch Alloy Wheels", "Hill Hold Assist", "ESP"
    ]
},{
    "car_model": "Fronx", "name": "Zeta Turbo AT",
    "fuel": "Petrol", "transmission": "Automatic",
    "price_ex_showroom_inr": 1099000, "price_on_road_inr": 1252000,
    "mileage": 20.01, "mileage_unit": "kmpl",
    "power_bhp": 98.7, "torque_nm": 147.6,
    "key_features": [
        "Paddle Shifters", "Rear View Camera",
        "Wireless Charger", "Rear AC Vents", "Chrome Plated Inside Door Handles"
    ]
},{
    "car_model": "Fronx", "name": "Alpha Turbo DT AT",
    "fuel": "Petrol", "transmission": "Automatic",
    "price_ex_showroom_inr": 1198000, "price_on_road_inr": 1369679,
    "mileage": 20.01, "mileage_unit": "kmpl",
    "power_bhp": 98.7, "torque_nm": 147.6,
    "key_features": [
        "360 View Camera", "Head-Up Display (HUD)",
        "9-inch SmartPlay Pro+ Infotainment", "Dual Tone Exterior", "Cruise Control"
    ]
},

    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  DZIRE  VARIANTS  (CarDekho maruti/dzire — ex-showroom / on-road Delhi)
    # ╚══════════════════════════════════════════════════════════════════════════

    {
        "car_model": "Dzire", "name": "LXI",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 626000, "price_on_road_inr": 716785,
        "mileage": 24.79, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags (Standard)", "ABS + EBD", "Rear Parking Sensors",
            "Manual AC", "Halogen Headlamps", "ESC & Hill Hold Assist"
        ]
    },
    {
        "car_model": "Dzire", "name": "VXI",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 717000, "price_on_road_inr": 815000,
        "mileage": 24.79, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "6 Airbags", "Height Adjustable Driver Seat",
            "7-inch Touchscreen", "Wireless Android Auto & Apple CarPlay", "Rear AC Vents"
        ]
    },
    {
        "car_model": "Dzire", "name": "VXI AMT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 762000, "price_on_road_inr": 865000,
        "mileage": 25.71, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "AMT Gearbox", "6 Airbags", "Idle Start-Stop",
            "7-inch Touchscreen", "Wireless Android Auto & Apple CarPlay"
        ]
    },
    {
        "car_model": "Dzire", "name": "VXI CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 803000, "price_on_road_inr": 905000,
        "mileage": 33.73, "mileage_unit": "km/kg",
        "power_bhp": 68.80, "torque_nm": 101.8,
        "key_features": [
            "Factory S-CNG", "6 Airbags", "7-inch Touchscreen",
            "Wireless Android Auto & Apple CarPlay"
        ]
    },
    {
        "car_model": "Dzire", "name": "ZXI",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 818000, "price_on_road_inr": 925000,
        "mileage": 24.79, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "LED Headlamps & DRLs", "15-inch Alloy Wheels",
            "Auto Climate Control", "Push Button Start", "TPMS"
        ]
    },
    {
        "car_model": "Dzire", "name": "ZXI AMT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 863000, "price_on_road_inr": 975000,
        "mileage": 25.71, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "AMT Gearbox", "LED Headlamps", "15-inch Alloy Wheels",
            "Auto Climate Control", "Hill Hold Assist"
        ]
    },
    {
        "car_model": "Dzire", "name": "ZXI Plus",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 886000, "price_on_road_inr": 1005000,
        "mileage": 24.79, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "9-inch SmartPlay Pro+ Touchscreen", "Wireless Charger",
            "Cruise Control", "Electric Sunroof", "360 Degree Camera"
        ]
    },
    {
        "car_model": "Dzire", "name": "ZXI CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 904000, "price_on_road_inr": 1025000,
        "mileage": 33.73, "mileage_unit": "km/kg",
        "power_bhp": 68.80, "torque_nm": 101.8,
        "key_features": [
            "Factory S-CNG", "LED Headlamps", "15-inch Alloy Wheels",
            "Auto Climate Control", "Rear AC Vents"
        ]
    },
    {
        "car_model": "Dzire", "name": "ZXI Plus AMT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 931000, "price_on_road_inr": 1055000,
        "mileage": 25.71, "mileage_unit": "kmpl",
        "power_bhp": 80.46, "torque_nm": 111.7,
        "key_features": [
            "AMT Gearbox", "9-inch Touchscreen", "Wireless Charger",
            "Sunroof", "360 Degree Camera"
        ]
    },

    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  INVICTO  VARIANTS  (CarDekho maruti/invicto)
    # ╚══════════════════════════════════════════════════════════════════════════
    {
        "car_model": "Invicto", "name": "Zeta Plus 7Str",
        "fuel": "Hybrid", "transmission": "CVT",
        "price_ex_showroom_inr": 2497000, "price_on_road_inr": 2897643,
        "mileage": 23.24, "mileage_unit": "kmpl",
        "power_bhp": 150.19, "torque_nm": 188.0,
        "key_features": [
            "Strong Hybrid 1987 cc", "e-CVT", "7-Seater Captain Seats",
            "6 Airbags", "8-inch Touchscreen", "Fabric Upholstery"
        ]
    },
    {
        "car_model": "Invicto", "name": "Zeta Plus 8Str",
        "fuel": "Hybrid", "transmission": "CVT",
        "price_ex_showroom_inr": 2502000, "price_on_road_inr": 2905000,
        "mileage": 23.24, "mileage_unit": "kmpl",
        "power_bhp": 150.19, "torque_nm": 188.0,
        "key_features": [
            "Strong Hybrid", "e-CVT", "8-Seater Bench Middle Row",
            "6 Airbags", "8-inch Touchscreen", "Fabric Upholstery"
        ]
    },
    {
        "car_model": "Invicto", "name": "Alpha Plus 7Str",
        "fuel": "Hybrid", "transmission": "CVT",
        "price_ex_showroom_inr": 2861000, "price_on_road_inr": 3315000,
        "mileage": 23.24, "mileage_unit": "kmpl",
        "power_bhp": 150.19, "torque_nm": 188.0,
        "key_features": [
            "Top Trim", "Strong Hybrid", "e-CVT", "7-Seater",
            "Panoramic Sunroof", "Ventilated Front Seats", 
            "360 Degree Camera", "Powered Tailgate", "Leatherette Upholstery"
        ]
    },
    # Victoris variants: CarDekho maruti/victoris/variants.htm (ex-showroom price ladder, Delhi)
    {
        "car_model": "Victoris", "name": "LXI",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1050000, "price_on_road_inr": 1144500,
        "mileage": 21.18, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "6 Airbags", "ABS + EBD + ESC",
            "Halogen Projector Headlamps", "Auto AC with Rear Vents",
            "Power Windows", "Rear Parking Sensors",
            "7-inch Touchscreen"
        ]
    },
    {
        "car_model": "Victoris", "name": "LXI CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 1150000, "price_on_road_inr": 1253500,
        "mileage": 27.02, "mileage_unit": "km/kg",
        "power_bhp": 87.83, "torque_nm": 121.5,
        "key_features": [
            "6 Airbags", "ABS + EBD + ESC",
            "Underbody CNG Tank", "Auto AC with Rear Vents",
            "Power Windows", "Rear Parking Sensors",
            "7-inch Touchscreen"
        ]
    },
    {
        "car_model": "Victoris", "name": "VXI",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1180000, "price_on_road_inr": 1286200,
        "mileage": 21.18, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "6 Airbags", "7-inch Touchscreen",
            "Android Auto & Apple CarPlay",
            "Rear Camera", "Steering Mounted Controls",
            "Auto AC", "Cruise Control"
        ]
    },
    {
        "car_model": "Victoris", "name": "VXI CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 1280000, "price_on_road_inr": 1395200,
        "mileage": 27.02, "mileage_unit": "km/kg",
        "power_bhp": 87.83, "torque_nm": 121.5,
        "key_features": [
            "6 Airbags", "7-inch Touchscreen",
            "Android Auto & Apple CarPlay",
            "Rear Camera", "Steering Mounted Controls",
            "Auto AC", "Cruise Control"
        ]
    },
    {
        "car_model": "Victoris", "name": "VXI AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1336000, "price_on_road_inr": 1456240,
        "mileage": 21.06, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "6 Airbags", "7-inch Touchscreen",
            "Paddle Shifters", "Rear Camera",
            "Steering Mounted Controls",
            "Auto AC", "Cruise Control"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1357000, "price_on_road_inr": 1479130,
        "mileage": 21.18, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "6 Airbags", "All-LED Headlights & DRLs",
            "10.25-inch Digital Driver Display",
            "Wireless Android Auto & Apple CarPlay",
            "Cruise Control", "Push Button Start",
            "17-inch All-Black Alloys", "Powered Tailgate"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI DT",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1372000, "price_on_road_inr": 1495480,
        "mileage": 21.18, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "Dual Tone Exterior", "All-LED Headlights & DRLs",
            "10.25-inch Digital Driver Display",
            "Wireless Android Auto & Apple CarPlay",
            "Cruise Control", "Push Button Start",
            "17-inch All-Black Alloys", "Powered Tailgate"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI (O)",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1408000, "price_on_road_inr": 1534720,
        "mileage": 21.18, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "6 Airbags", "Panoramic Sunroof",
            "10.25-inch Digital Driver Display",
            "Wireless Android Auto & Apple CarPlay",
            "Cruise Control", "Push Button Start",
            "Powered Tailgate", "Connected Car Tech"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI (O) DT",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1423000, "price_on_road_inr": 1551070,
        "mileage": 21.18, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "Dual Tone Exterior", "Panoramic Sunroof",
            "10.25-inch Digital Driver Display",
            "Wireless Android Auto & Apple CarPlay",
            "Cruise Control", "Push Button Start",
            "Powered Tailgate", "Connected Car Tech"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 1457000, "price_on_road_inr": 1588130,
        "mileage": 27.02, "mileage_unit": "km/kg",
        "power_bhp": 87.83, "torque_nm": 121.5,
        "key_features": [
            "6 Airbags", "All-LED Headlights",
            "10.25-inch Digital Driver Display",
            "Wireless Android Auto & Apple CarPlay",
            "Cruise Control", "Push Button Start",
            "17-inch All-Black Alloys", "Underbody CNG Tank"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI CNG DT",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 1472000, "price_on_road_inr": 1604480,
        "mileage": 27.02, "mileage_unit": "km/kg",
        "power_bhp": 87.83, "torque_nm": 121.5,
        "key_features": [
            "Dual Tone Exterior", "All-LED Headlights",
            "10.25-inch Digital Driver Display", "17-inch All-Black Alloys",
            "Cruise Control", "Push Button Start",
            "Wireless Android Auto & Apple CarPlay", "Underbody CNG Tank"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1513000, "price_on_road_inr": 1649170,
        "mileage": 21.06, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "6 Airbags", "Paddle Shifters",
            "10.25-inch Digital Driver Display", "Cruise Control",
            "Wireless Android Auto & Apple CarPlay",
            "Push Button Start", "17-inch All-Black Alloys", "Powered Tailgate"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1524000, "price_on_road_inr": 1661160,
        "mileage": 21.18, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "6 Airbags", "17-inch Dual-Tone Alloys",
            "10.1-inch Touchscreen",
            "Wireless Android Auto & Apple CarPlay",
            "360 Degree Camera", "Ventilated Seats",
            "Connected Car Tech", "8-speaker Infinity Sound System"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI AT DT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1528000, "price_on_road_inr": 1665520,
        "mileage": 21.06, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "Dual Tone Exterior", "Paddle Shifters",
            "10.25-inch Digital Driver Display", "Cruise Control",
            "Wireless Android Auto & Apple CarPlay",
            "Push Button Start", "17-inch All-Black Alloys", "Powered Tailgate"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus DT",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1539000, "price_on_road_inr": 1677510,
        "mileage": 21.18, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "Dual Tone Exterior", "17-inch Dual-Tone Alloys",
            "10.1-inch Touchscreen",
            "Wireless Android Auto & Apple CarPlay",
            "360 Degree Camera", "Ventilated Seats",
            "Connected Car Tech", "8-speaker Infinity Sound System"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI (O) AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1564000, "price_on_road_inr": 1704760,
        "mileage": 21.06, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "6 Airbags", "Panoramic Sunroof",
            "10.25-inch Digital Driver Display", "Paddle Shifters",
            "Cruise Control", "Push Button Start",
            "Powered Tailgate", "Connected Car Tech"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI (O) AT DT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1579000, "price_on_road_inr": 1721110,
        "mileage": 21.06, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "Dual Tone Exterior", "Panoramic Sunroof",
            "10.25-inch Digital Driver Display", "Paddle Shifters",
            "Cruise Control", "Push Button Start",
            "Powered Tailgate", "Connected Car Tech"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus (O)",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1582000, "price_on_road_inr": 1724380,
        "mileage": 21.18, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "Panoramic Sunroof", "8-way Powered Driver Seat",
            "10.1-inch Touchscreen", "Heads Up Display", 
            "360 Degree Camera", "Ventilated Seats", 
            "Connected Car Tech", "Powered Tailgate"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus (O) DT",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 1597000, "price_on_road_inr": 1740730,
        "mileage": 21.18, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "Dual Tone Exterior", "Panoramic Sunroof", 
            "Heads Up Display", "10.1-inch Touchscreen",
            "360 Degree Camera", "Ventilated Seats",
            "Powered Tailgate", "8-way Powered Driver Seat"
        ]
    },
    {
        "car_model": "Victoris", "name": "VXI Strong Hybrid",
        "fuel": "Hybrid", "transmission": "Automatic",
        "price_ex_showroom_inr": 1638000, "price_on_road_inr": 1785420,
        "mileage": 28.65, "mileage_unit": "kmpl",
        "power_bhp": 114.4, "torque_nm": 141.0,
        "key_features": [
            "Strong Hybrid System", "e-CVT Transmission",
            "6 Airbags", "10.25-inch Digital Driver Display",
            "Auto AC with Rear Vents", "Connected LED Tail Lamps",
            "Keyless Entry", "Regenerative Braking"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1719000, "price_on_road_inr": 1873710,
        "mileage": 21.06, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "Level 2 ADAS", "17-inch Dual-Tone Alloys",
            "10.1-inch Touchscreen", "Paddle Shifters", 
            "360 Degree Camera", "Ventilated Seats", 
            "Connected Car Tech", "8-speaker Infinity Sound System"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus AT DT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1734000, "price_on_road_inr": 1890060,
        "mileage": 21.06, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "Level 2 ADAS", "Dual Tone Exterior", 
            "10.1-inch Touchscreen", "Paddle Shifters", 
            "360 Degree Camera", "Ventilated Seats", 
            "Connected Car Tech", "8-speaker Infinity Sound System"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus (O) AT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1777000, "price_on_road_inr": 1936930,
        "mileage": 21.06, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "Level 2 ADAS", "Panoramic Sunroof",
            "10.1-inch Touchscreen", "Paddle Shifters", 
            "360 Degree Camera", "Heads Up Display", 
            "Ventilated Seats", "Powered Tailgate"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Strong Hybrid",
        "fuel": "Hybrid", "transmission": "Automatic",
        "price_ex_showroom_inr": 1780000, "price_on_road_inr": 1940200,
        "mileage": 28.65, "mileage_unit": "kmpl",
        "power_bhp": 114.4, "torque_nm": 141.0,
        "key_features": [
            "Strong Hybrid System", "e-CVT Transmission",
            "10.25-inch Digital Driver Display", "All-LED Headlights",
            "Wireless Phone Mirroring", "Cruise Control",
            "17-inch All-Black Alloys", "Regenerative Braking"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus (O) AT DT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1792000, "price_on_road_inr": 1953280,
        "mileage": 21.06, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "Dual Tone Exterior", "Level 2 ADAS",
            "Panoramic Sunroof", "10.1-inch Touchscreen",
            "Paddle Shifters", "360 Degree Camera",
            "Heads Up Display", "Powered Tailgate"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Strong Hybrid DT",
        "fuel": "Hybrid", "transmission": "Automatic",
        "price_ex_showroom_inr": 1795000, "price_on_road_inr": 1956550,
        "mileage": 28.65, "mileage_unit": "kmpl",
        "power_bhp": 114.4, "torque_nm": 141.0,
        "key_features": [
            "Dual Tone Exterior", "Strong Hybrid System",
            "e-CVT Transmission", "10.25-inch Digital Driver Display",
            "Wireless Phone Mirroring", "Cruise Control",
            "17-inch All-Black Alloys", "Regenerative Braking"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI (O) Strong Hybrid",
        "fuel": "Hybrid", "transmission": "Automatic",
        "price_ex_showroom_inr": 1839000, "price_on_road_inr": 2004510,
        "mileage": 28.65, "mileage_unit": "kmpl",
        "power_bhp": 114.4, "torque_nm": 141.0,
        "key_features": [
            "Strong Hybrid System", "Panoramic Sunroof",
            "10.25-inch Digital Driver Display", "Powered Tailgate",
            "Connected Car Tech", "Cruise Control",
            "17-inch All-Black Alloys", "e-CVT Gearbox"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI (O) Strong Hybrid DT",
        "fuel": "Hybrid", "transmission": "Automatic",
        "price_ex_showroom_inr": 1854000, "price_on_road_inr": 2020860,
        "mileage": 28.65, "mileage_unit": "kmpl",
        "power_bhp": 114.4, "torque_nm": 141.0,
        "key_features": [
            "Dual Tone Exterior", "Strong Hybrid System",
            "Panoramic Sunroof", "10.25-inch Digital Driver Display",
            "Powered Tailgate", "Connected Car Tech",
            "e-CVT Gearbox", "Cooled Wireless Charging"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus AT AWD",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1864000, "price_on_road_inr": 2031760,
        "mileage": 19.07, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "All-Wheel Drive (AWD)", "Hill Descent Control",
            "Level 2 ADAS", "10.1-inch Touchscreen",
            "360 Degree Camera", "Ventilated Seats",
            "Paddle Shifters", "Connected Car Tech"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus AWD AT DT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1879000, "price_on_road_inr": 2048110,
        "mileage": 19.07, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "Dual Tone Exterior", "All-Wheel Drive (AWD)",
            "Level 2 ADAS", "10.1-inch Touchscreen",
            "360 Degree Camera", "Ventilated Seats",
            "Paddle Shifters", "Connected Car Tech"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus (O) AT AWD",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1922000, "price_on_road_inr": 2094980,
        "mileage": 19.07, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "All-Wheel Drive (AWD)", "Level 2 ADAS",
            "Panoramic Sunroof", "10.1-inch Touchscreen",
            "Heads Up Display", "360 Degree Camera",
            "Powered Tailgate", "Hill Descent Control"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus (O) AWD AT DT",
        "fuel": "Petrol", "transmission": "Automatic",
        "price_ex_showroom_inr": 1937000, "price_on_road_inr": 2111330,
        "mileage": 19.07, "mileage_unit": "kmpl",
        "power_bhp": 101.64, "torque_nm": 139,
        "key_features": [
            "Dual Tone Exterior", "All-Wheel Drive (AWD)",
            "Level 2 ADAS", "Panoramic Sunroof",
            "10.1-inch Touchscreen", "Heads Up Display",
            "360 Degree Camera", "Powered Tailgate"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus Strong Hybrid",
        "fuel": "Hybrid", "transmission": "Automatic",
        "price_ex_showroom_inr": 1947000, "price_on_road_inr": 2122230,
        "mileage": 28.65, "mileage_unit": "kmpl",
        "power_bhp": 114.4, "torque_nm": 141.0,
        "key_features": [
            "Strong Hybrid System", "17-inch Dual-Tone Alloys",
            "10.1-inch Touchscreen",
            "Ventilated Seats", "360 Degree Camera",
            "Infinity 8-speaker Audio", "Connected Car Tech",
            "e-CVT Transmission"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus Strong Hybrid DT",
        "fuel": "Hybrid", "transmission": "Automatic",
        "price_ex_showroom_inr": 1962000, "price_on_road_inr": 2138580,
        "mileage": 28.65, "mileage_unit": "kmpl",
        "power_bhp": 114.4, "torque_nm": 141.0,
        "key_features": [
            "Dual Tone Exterior", "Strong Hybrid System",
            "17-inch Dual-Tone Alloys", "10.1-inch Touchscreen",
            "Ventilated Seats", "360 Degree Camera",
            "Premium Audio System", "e-CVT Transmission"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus (O) Strong Hybrid DT",
        "fuel": "Hybrid", "transmission": "Automatic",
        "price_ex_showroom_inr": 1999000, "price_on_road_inr": 2178910,
        "mileage": 28.65, "mileage_unit": "kmpl",
        "power_bhp": 114.4, "torque_nm": 141.0,
        "key_features": [
            "Dual Tone Exterior", "Panoramic Sunroof",
            "10.1-inch Touchscreen", "Heads Up Display",
            "360 Degree Camera", "Powered Tailgate", 
            "Strong Hybrid System", "Ventilated Seats"
        ]
    },
    {
        "car_model": "Victoris", "name": "ZXI Plus (O) Strong Hybrid",
        "fuel": "Hybrid", "transmission": "Automatic",
        "price_ex_showroom_inr": 1999000, "price_on_road_inr": 2178910,
        "mileage": 28.65, "mileage_unit": "kmpl",
        "power_bhp": 114.4, "torque_nm": 141.0,
        "key_features": [
            "Panoramic Sunroof", "10.1-inch Touchscreen",
            "Heads Up Display", "360 Degree Camera",
            "Powered Tailgate", "Strong Hybrid System",
            "Ventilated Seats", "8-way Powered Driver Seat"
        ]
    },

    # e Vitara — ex-showroom & ARAI range per India launch; torque 192.5 Nm (Maruti spec)
    {
        "car_model": "e Vitara", "name": "Delta 49 kWh",
        "fuel": "Electric", "transmission": "Automatic",
        "price_ex_showroom_inr": 1599000, "price_on_road_inr": 1683059,
        "mileage": 440.0, "mileage_unit": "km/charge",
        "power_bhp": 142.0, "torque_nm": 192.5,
        "key_features": [
            "49 kWh battery", "ARAI range 440 km", "7 Airbags", 
            "10.25-inch Touchscreen", "Wireless Android Auto & Apple CarPlay", 
            "Digital Instrument Cluster", "18-inch Aerodynamic Alloy Wheels", 
            "Infinity Sound System", "Automatic Climate Control", 
            "Electronic Parking Brake"
        ]
    },
    {
        "car_model": "e Vitara", "name": "Zeta 61 kWh",
        "fuel": "Electric", "transmission": "Automatic",
        "price_ex_showroom_inr": 1749000, "price_on_road_inr": 1840000,
        "mileage": 543.0, "mileage_unit": "km/charge",
        "power_bhp": 172.0, "torque_nm": 192.5,
        "key_features": [
            "61 kWh battery", "ARAI range 543 km", "7 Airbags", 
            "10.25-inch Touchscreen", "Wireless Android Auto & Apple CarPlay", 
            "Reverse Parking Camera", "Wireless Phone Charger", 
            "Infinity Sound System", "Electronic Parking Brake", 
            "18-inch Alloy Wheels"
        ]
    },
    {
        "car_model": "e Vitara", "name": "Alpha 61 kWh",
        "fuel": "Electric", "transmission": "Automatic",
        "price_ex_showroom_inr": 1979000, "price_on_road_inr": 2080000,
        "mileage": 543.0, "mileage_unit": "km/charge",
        "power_bhp": 172.0, "torque_nm": 192.5,
        "key_features": [
            "61 kWh battery", "ARAI range 543 km", "Level-2 ADAS", 
            "360-degree Camera", "Ventilated Front Seats", 
            "10-way Power Adjustable Driver Seat", "Single-pane Glass Roof", 
            "Semi-leatherette Seats", "Projector LED Headlamps", 
            "10.25-inch Touchscreen", "Wireless Phone Charger"
        ]
    },
    {
        "car_model": "e Vitara", "name": "Alpha Dual Tone 61 kWh",
        "fuel": "Electric", "transmission": "Automatic",
        "price_ex_showroom_inr": 2001000, "price_on_road_inr": 2103000,
        "mileage": 543.0, "mileage_unit": "km/charge",
        "power_bhp": 172.0, "torque_nm": 192.5,
        "key_features": [
            "61 kWh battery", "ARAI range 543 km", "Dual-Tone Exterior", 
            "Level-2 ADAS", "360-degree Camera", "Ventilated Front Seats", 
            "10-way Power Adjustable Driver Seat", "Single-pane Glass Roof", 
            "Semi-leatherette Seats", "Projector LED Headlamps", 
            "10.25-inch Touchscreen"
        ]
    },

    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  DZIRE TOUR S  (CarDekho maruti/dzire-tour-s)
    # ╚══════════════════════════════════════════════════════════════════════════
    {
        "car_model": "Dzire Tour S", "name": "STD",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 624000, "price_on_road_inr": 728000,
        "mileage": 26.06, "mileage_unit": "kmpl",
        "power_bhp": 80.00, "torque_nm": 111.7,
        "key_features": [
            "Speed Limiting Device (80 km/h)",
            "6 Airbags",
            "ABS with EBD and Brake Assist",
            "Reverse Parking Sensors",
            "Electronic Stability Program (ESP)",
            "Manual Air Conditioning",
            "Front Power Windows",
            "Engine Immobilizer",
            "Steel Rims with Center Cap",
            "Tilt Adjustable Steering"
        ]
    },
    {
        "car_model": "Dzire Tour S", "name": "CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 710000, "price_on_road_inr": 798000,
        "mileage": 34.3, "mileage_unit": "km/kg",
        "power_bhp": 69.00, "torque_nm": 101.8,
        "key_features": [
            "Factory-fitted S-CNG Kit",
            "Speed Limiting Device (80 km/h)",
            "6 Airbags",
            "ABS with EBD",
            "Reverse Parking Sensors",
            "Manual Air Conditioning",
            "Digital Instrument Cluster with CNG Fuel Gauge",
            "Engine Immobilizer",
            "Front Power Windows",
            "Speed Sensitive Auto Door Lock"
        ]
    },
    # ── Maruti Suzuki Eeco Cargo ──────────────────────────────────────────────
    {
        "car_model": "Eeco Cargo", "name": "STD",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 539000, "price_on_road_inr": 592936,
        "mileage": 20.2, "mileage_unit": "kmpl",
        "power_bhp": 79.65, "torque_nm": 104.4,
        "key_features": [
            "Spacious Flat Cargo Bed", 
            "Driver Airbag", 
            "ABS with EBD", 
            "Reverse Parking Sensors", 
            "Engine Immobilizer", 
            "Cabin Heater", 
            "Integrated Headrests", 
            "High Mount Stop Lamp"
        ]
    },
    {
        "car_model": "Eeco Cargo", "name": "STD CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 621000, "price_on_road_inr": 685000,
        "mileage": 27.05, "mileage_unit": "km/kg",
        "power_bhp": 70.67, "torque_nm": 95.0,
        "key_features": [
            "Factory Fitted S-CNG Kit", 
            "Driver Airbag", 
            "ABS with EBD", 
            "Reverse Parking Sensors", 
            "Digital Instrument Cluster with CNG Gauge", 
            "Flat Cargo Floor", 
            "Engine Immobilizer"
        ]
    },
    {
        "car_model": "Eeco Cargo", "name": "STD AC CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 661000, "price_on_road_inr": 728000,
        "mileage": 27.05, "mileage_unit": "km/kg",
        "power_bhp": 70.67, "torque_nm": 95.0,
        "key_features": [
            "Manual Air Conditioning", 
            "Factory Fitted S-CNG Kit", 
            "Driver Airbag", 
            "ABS with EBD", 
            "Reverse Parking Sensors", 
            "Cabin Heater", 
            "Digital Instrument Cluster"
        ]
    },

    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  EECO TOUR V  (Fleet Passenger Van)
    # ╚══════════════════════════════════════════════════════════════════════════
    {
        "car_model": "Eeco Tour V", "name": "5 Seater STD",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 518000, "price_on_road_inr": 570646,
        "mileage": 19.71, "mileage_unit": "kmpl",
        "power_bhp": 79.65, "torque_nm": 104.4,
        "key_features": [
            "6 Airbags (Standard)", 
            "Speed Limiting Device (80 km/h)", 
            "ABS with EBD", 
            "Reverse Parking Sensors", 
            "Child Lock for Sliding Doors", 
            "Cabin Heater", 
            "Integrated Headrests"
        ]
    },
    {
        "car_model": "Eeco Tour V", "name": "6 Seater STD",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 546000, "price_on_road_inr": 615000,
        "mileage": 19.71, "mileage_unit": "kmpl",
        "power_bhp": 79.65, "torque_nm": 104.4,
        "key_features": [
            "6-Seater Capacity", 
            "6 Airbags", 
            "Speed Limiting Device (80 km/h)", 
            "ABS with EBD", 
            "Reverse Parking Sensors", 
            "Child Lock for Sliding Doors", 
            "Cabin Heater"
        ]
    },
    {
        "car_model": "Eeco Tour V", "name": "5 Seater AC",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 551000, "price_on_road_inr": 625000,
        "mileage": 19.71, "mileage_unit": "kmpl",
        "power_bhp": 79.65, "torque_nm": 104.4,
        "key_features": [
            "Manual Air Conditioning", 
            "6 Airbags", 
            "Speed Limiting Device (80 km/h)", 
            "ABS with EBD", 
            "Reverse Parking Sensors", 
            "Child Lock for Sliding Doors", 
            "Cabin Heater"
        ]
    },
    {
        "car_model": "Eeco Tour V", "name": "5 Seater AC CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 633000, "price_on_road_inr": 718000,
        "mileage": 26.78, "mileage_unit": "km/kg",
        "power_bhp": 70.67, "torque_nm": 95.0,
        "key_features": [
            "Factory Fitted S-CNG Kit", 
            "Manual Air Conditioning", 
            "6 Airbags", 
            "Speed Limiting Device (80 km/h)", 
            "ABS with EBD", 
            "Reverse Parking Sensors", 
            "Digital Instrument Cluster with CNG Gauge"
        ]
    },

    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  ERTIGA TOUR (Tour M)
    # ╚══════════════════════════════════════════════════════════════════════════
    {
        "car_model": "Ertiga Tour", "name": "STD",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 968000, "price_on_road_inr": 1083940,
        "mileage": 18.04, "mileage_unit": "kmpl",
        "power_bhp": 103.25, "torque_nm": 138.0,
        "key_features": [
            "Speed Limiting Device (80 km/h)",
            "7-Seater Passenger Configuration",
            "Dual Front Airbags",
            "ABS with EBD and Brake Assist",
            "Reverse Parking Sensors",
            "Manual Air Conditioning",
            "Power Steering with Tilt Adjustment",
            "Multi-Information Display (MID)",
            "Body-Coloured Bumpers",
            "Engine Immobilizer"
        ]
    },
    {
        "car_model": "Ertiga Tour", "name": "STD CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 1059000, "price_on_road_inr": 1185000,
        "mileage": 26.08, "mileage_unit": "km/kg",
        "power_bhp": 91.18, "torque_nm": 122.0,
        "key_features": [
            "Factory-fitted S-CNG Kit",
            "Speed Limiting Device (80 km/h)",
            "7-Seater Configuration",
            "Dual Front Airbags",
            "ABS with EBD",
            "Manual AC with Rear Vents",
            "Reverse Parking Sensors",
            "Digital Instrument Cluster with CNG Gauge",
            "Idle Start-Stop System (Petrol mode)",
            "Power Steering"
        ]
    },
    # ╔══════════════════════════════════════════════════════════════════════════
    # ║  WAGON R TOUR (Tour H3)
    # ╚══════════════════════════════════════════════════════════════════════════
    {
        "car_model": "Wagon R Tour", "name": "H3 PETROL",
        "fuel": "Petrol", "transmission": "Manual",
        "price_ex_showroom_inr": 499000, "price_on_road_inr": 544239,
        "mileage": 25.4, "mileage_unit": "kmpl",
        "power_bhp": 65.71, "torque_nm": 89.0,
        "key_features": [
            "Speed Limiting Device (80 km/h)",
            "Dual Front Airbags",
            "ABS with EBD",
            "Reverse Parking Sensors",
            "Manual Air Conditioning with Heater",
            "Front Power Windows",
            "Idle Start-Stop System",
            "Central Locking",
            "Body-Coloured Bumpers"
        ]
    },
    {
        "car_model": "Wagon R Tour", "name": "H3 CNG",
        "fuel": "CNG", "transmission": "Manual",
        "price_ex_showroom_inr": 589000, "price_on_road_inr": 642000,
        "mileage": 34.73, "mileage_unit": "km/kg",
        "power_bhp": 55.92, "torque_nm": 82.1,
        "key_features": [
            "Factory-fitted S-CNG Kit",
            "Speed Limiting Device (80 km/h)",
            "Dual Front Airbags",
            "ABS with EBD",
            "Reverse Parking Sensors",
            "Manual AC with Cabin Heater",
            "Digital Instrument Cluster",
            "Front Power Windows",
            "Engine Immobilizer",
            "Speed Sensitive Auto Door Lock"
        ]
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
#  INSERT  FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def insert_cars():
    db = get_db()
    col = db["cars"]
    for raw in CARS:
        try:
            car = Car.model_validate(raw)
        except ValidationError as e:
            print(f"❌ Car validation failed: {raw.get('make')} {raw.get('model')}\n{e}")
            continue
        doc = car.model_dump(by_alias=True)
        exists = col.find_one({"make": doc["make"], "model": doc["model"]})
        if not exists:
            result = col.insert_one(doc)
            print(f"✅ Car inserted : {doc['make']} {doc['model']} → {result.inserted_id}")
        else:
            print(f"⚠️  Skipped      : {doc['make']} {doc['model']} (already exists)")


def insert_variants():
    db = get_db()
    cars_col = db["cars"]
    variants_col = db["variants"]

    for raw in VARIANTS:
        try:
            v = VariantSeed.model_validate(raw)
        except ValidationError as e:
            print(
                f"❌ Variant validation failed: "
                f"{raw.get('car_model')} {raw.get('name')}\n{e}"
            )
            continue

        car = cars_col.find_one({"model": v.car_model})
        if not car:
            print(f"❌ Car not found : {v.car_model} — skipping variant '{v.name}'")
            continue

        exists = variants_col.find_one({"car_id": car["_id"], "name": v.name})
        if not exists:
            payload = v.model_dump(exclude={"car_model"}, exclude_none=True, by_alias=True)
            payload["car_id"] = car["_id"]
            result = variants_col.insert_one(payload)
            print(f"✅ Variant inserted : {v.car_model} {v.name} → {result.inserted_id}")
        else:
            print(f"⚠️  Skipped         : {v.car_model} {v.name} (already exists)")


# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    insert_cars()
    insert_variants()