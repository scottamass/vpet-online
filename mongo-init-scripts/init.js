// init.js

// Use the 'monsterdb' database
db = db.getSiblingDB('monsterdb');

// Create a 'monsters' collection and insert data
db.monsters.insert(
    [{
        "_id": {
          "$oid": "653f8cce640e51541f581adb"
        },
        "id": 1,
        "name": "botamon",
        "slot": "a",
        "power": 4,
        "hp": null,
        "atk": null,
        "evolve": 2,
        "stage": 1
      },
      {
        "_id": {
          "$oid": "6540a5b3640e51541f581ae9"
        },
        "id": 2,
        "name": "koromon",
        "slot": "b",
        "power": 4,
        "hp": null,
        "atk": null,
        "evolvea": 3,
        "evolveb": 4,
        "stage": 2
      },
      {
        "_id": {
          "$oid": "65413ac740f36a4bb466d822"
        },
        "id": 999,
        "name": "MissingNo",
        "slot": "j",
        "power": 220,
        "hp": 20,
        "atk": 5,
        "evolvea": null,
        "evolveb": null,
        "stage": 5
      },
      {
        "_id": {
          "$oid": "65450c27640e51541f581aff"
        },
        "id": 3,
        "name": "agumon",
        "slot": "b",
        "power": 15,
        "hp": 5,
        "atk": 1,
        "evolvea": 6,
        "evolveb": 7,
        "evolvec": 8,
        "stage": 3
      },
      {
        "_id": {
          "$oid": "65450d7f640e51541f581b00"
        },
        "id": 4,
        "name": "agumon(black)",
        "slot": "b",
        "power": 15,
        "hp": 5,
        "atk": 1,
        "evolvea": 6,
        "evolveb": 7,
        "evolvec": 8,
        "stage": 3
      }]
  // Add more data as needed
);
