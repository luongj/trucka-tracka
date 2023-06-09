# trucka-tracka
- exercise based on [`peck / engineering-assessment`](https://github.com/peck/engineering-assessment)
- naming inspired by [tiki-taka](https://en.wikipedia.org/wiki/Tiki-taka)

## Dataset Characteristics

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
SELECT Status, COUNT(*) AS count
FROM Mobile_Food_Facility_Permit
GROUP BY Status
ORDER BY Status ASC

=> 
"Status"	"count"
"APPROVED"	"60"
"EXPIRED"	"369"
"ISSUED"	"2"
"REQUESTED"	"193"
"SUSPEND"	"5"
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

## The "Problem"

*I want to go on a taco crawl, but I don't want to spend much time. Where would I go to find the highest concentration of taco trucks?"*

## The Solution

*The system should tell the user where they're LIKELY to find the highest density of their desired. Mobile food vendors have less consistent hours. They are also mobile.* 

- Ask the user what they're looking for, and what they consider close by (in feet).
- Determine all the locations that have said food item (eg. "taco") in the `FoodItems` field.
- Iterate through the `location` list and determine how many in their set are within specified distance. Ignore the same `permit` value.
- Render a result set sorted by most within specified distance.

## The Future Perfect
- Distances are as the crow flies, which is pragmatically less useful.
- Multiple truck locations are not counted for the truck being evaluated, but multiple truck locations *ARE* being calculated for proximity calculations.
- Not much in the way of data validation.