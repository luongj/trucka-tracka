# trucka-tracka
- exercise based on `peck / engineering-assessment`
- naming inspired by [tiki-taka](https://en.wikipedia.org/wiki/Tiki-taka)

### Dataset Characteristics

**COLUMN: `permit` and `locationid`**

Each row has a unique `locationid`, and non-unique `permit` value. Example: permit `21MFF-00128` belongs to `BH & MT LLC` and has `8` `APPROVED` locations each with a separate `locationid`. 
```
SELECT COUNT(*) 
FROM Mobile_Food_Facility_Permit
=> 629
```

```
SELECT DISTINCT locationid 
FROM Mobile_Food_Facility_Permit
=> 629
```

```
SELECT DISTINCT permit 
FROM Mobile_Food_Facility_Permit
=> 190
```

**COLUMN: `Status`** 

The values of the `status` column. 
```
SELECT DISTINCT Status 
FROM Mobile_Food_Facility_Permit

=>
"APPROVED"
"REQUESTED"
"EXPIRED"
"ISSUED"
"SUSPEND"
```

**COLUMN: `FoodItems`** 

The column that describes offerings is free text with inconsistent delimiters, making it difficult to create structured data from it.

Examples:
```
SELECT FoodItems 
FROM Mobile_Food_Facility_Permit 
ORDER BY RANDOM() LIMIT 5

=>
"Jerk chicken: curry chicken: curry goat: curry dhal: Burritos: Fish: Ox tails: rice: beans: veggies."
"Ice Cream: Pre-Packaged Chips: Candies: Bottled Water & Canned SODA"
"Cold Truck: Sandwiches: Noodles:  Pre-packaged Snacks: Candy: Desserts Various Beverages"
"Cold Truck: Soda:Chips:Candy: Cold/Hot Sandwiches: Donuts.  (Pitco Wholesale)"
"Cold Truck: Pre-packaged sandwiches: snacks: fruit: various beverages"
```

