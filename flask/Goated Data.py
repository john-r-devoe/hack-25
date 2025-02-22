import pandas as pd
import numpy as np

my_dict=
{
“location”: {
“lat”: 33.7767245106216,
“lng”: -84.38782520000001
},
“metrics”: {
“total_businesses”: 75,
“average_rating”: 2.64,
“average_distance”: 0.19,
“total_foot_traffic”: 25278,
“success_index”: 23.68,
“daily_walking_volume”: 14634,
“peak_hours_traffic”: 2926,
“visual_coverage”: “10 panoramic views of top-rated businesses”,
“total_searched_types”: 12,
“total_unique_places_found”: 75
},
“businesses”: [
{
“name”: “Boho Taco”,
“type”: [],
“rating”: 4.7,
“reviews”: 198,
“foot_traffic”: 207,
“distance”: 0.01,
“vicinity”: “22 5th Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Acuity Brands Plaza”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 81,
“distance”: 0.03,
“vicinity”: “Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Creative Destruction Lab - Atlanta”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 295,
“distance”: 0.03,
“vicinity”: “800 West Peachtree Street Northwest Room 4135, Suite 422, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Scheller College of Business”,
“type”: [],
“rating”: 4.7,
“reviews”: 50,
“foot_traffic”: 507,
“distance”: 0.03,
“vicinity”: “800 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Ray’s New York Pizza”,
“type”: [],
“rating”: 4.2,
“reviews”: 813,
“foot_traffic”: 282,
“distance”: 0.04,
“vicinity”: “26 5th Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Center for Paper Business and Industry Studies”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 123,
“distance”: 0.04,
“vicinity”: “800 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Starbucks”,
“type”: [],
“rating”: 3.6,
“reviews”: 182,
“foot_traffic”: 352,
“distance”: 0.05,
“vicinity”: “48 5th Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Bella Fine Homes00b”,
“type”: [],
“rating”: 5,
“reviews”: 5,
“foot_traffic”: 549,
“distance”: 0.06,
“vicinity”: “2870 West Peachtree Street Northwest #803, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Barnes & Noble at Georgia Tech”,
“type”: [],
“rating”: 4.4,
“reviews”: 1701,
“foot_traffic”: 445,
“distance”: 0.07,
“vicinity”: “48 5th Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “DTJ Design”,
“type”: [],
“rating”: 5,
“reviews”: 2,
“foot_traffic”: 681,
“distance”: 0.07,
“vicinity”: “817 West Peachtree Street Northwest Ste. 320, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “NFANT Labs”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 532,
“distance”: 0.07,
“vicinity”: “817 West Peachtree Street Northwest Ste. 320, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Wilkes Shelby R MD”,
“type”: [],
“rating”: 2.3,
“reviews”: 3,
“foot_traffic”: 374,
“distance”: 0.07,
“vicinity”: “830 West Peachtree Street Northwest #100, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “West Peachtree St at 5th St”,
“type”: [],
“rating”: 4,
“reviews”: 1,
“foot_traffic”: 444,
“distance”: 0.08,
“vicinity”: “United States”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Switchyards Midtown”,
“type”: [],
“rating”: 4.5,
“reviews”: 12,
“foot_traffic”: 197,
“distance”: 0.08,
“vicinity”: “817 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Pursuant Health”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 377,
“distance”: 0.08,
“vicinity”: “817 West Peachtree Street Northeast SUITE M-105, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “eQuoto”,
“type”: [],
“rating”: 3.7,
“reviews”: 15,
“foot_traffic”: 369,
“distance”: 0.08,
“vicinity”: “817 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Nexza, Inc.”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 510,
“distance”: 0.08,
“vicinity”: “817 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “ChargePoint Charging Station”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 366,
“distance”: 0.08,
“vicinity”: “715 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Highlands”,
“type”: [],
“rating”: 4,
“reviews”: 2,
“foot_traffic”: 172,
“distance”: 0.09,
“vicinity”: “817 West Peachtree Street Northwest #450, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Digital Scientists”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 363,
“distance”: 0.09,
“vicinity”: “817 West Peachtree Street Northwest #920, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Caleris Solutions, (Printing, Pack & Ship, Promotional Products)”,
“type”: [],
“rating”: 3.2,
“reviews”: 15,
“foot_traffic”: 282,
“distance”: 0.1,
“vicinity”: “817 West Peachtree Street Northwest Suite A180 404, Inside Biltmore Offices Bldg, 9667 876 Suite A180, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Atwoods Pizza Cafe”,
“type”: [],
“rating”: 4.5,
“reviews”: 987,
“foot_traffic”: 425,
“distance”: 0.11,
“vicinity”: “817 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Depasquale John M MD”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 182,
“distance”: 0.12,
“vicinity”: “845 Spring Street Northwest # B1, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “AT&T Store”,
“type”: [],
“rating”: 4,
“reviews”: 249,
“foot_traffic”: 693,
“distance”: 0.13,
“vicinity”: “62 5th Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Tea Leaf and Creamery (GT)”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 477,
“distance”: 0.14,
“vicinity”: “75 5th Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Penguin Computing”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 468,
“distance”: 0.14,
“vicinity”: “75 5th Street Northwest STE 3130, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Aviva by Kameel Midtown”,
“type”: [],
“rating”: 4.8,
“reviews”: 491,
“foot_traffic”: 622,
“distance”: 0.14,
“vicinity”: “756 West Peachtree Street Northwest suite G, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Tech Square Tavern”,
“type”: [],
“rating”: 4.5,
“reviews”: 2,
“foot_traffic”: 94,
“distance”: 0.14,
“vicinity”: “800 Spring Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Asian Fusion”,
“type”: [],
“rating”: 4.9,
“reviews”: 260,
“foot_traffic”: 627,
“distance”: 0.14,
“vicinity”: “75 5th Street Northwest #170, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “PNC Bank”,
“type”: [],
“rating”: 3.2,
“reviews”: 47,
“foot_traffic”: 462,
“distance”: 0.14,
“vicinity”: “75 5th Street Northwest A, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “AL Auto”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 506,
“distance”: 0.15,
“vicinity”: “855 West Peachtree Street Northwest suite 1523, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Waffle House”,
“type”: [],
“rating”: 3.9,
“reviews”: 1475,
“foot_traffic”: 323,
“distance”: 0.15,
“vicinity”: “66 5th Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Dr. Dominic C. Cruz, MD”,
“type”: [],
“rating”: 4,
“reviews”: 1,
“foot_traffic”: 93,
“distance”: 0.15,
“vicinity”: “855 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Buffalo Wild Wings ‘GO’”,
“type”: [],
“rating”: 2.9,
“reviews”: 182,
“foot_traffic”: 371,
“distance”: 0.16,
“vicinity”: “68 5th Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “El Burro Pollo”,
“type”: [],
“rating”: 4.3,
“reviews”: 102,
“foot_traffic”: 504,
“distance”: 0.16,
“vicinity”: “756 West Peachtree Street Northwest #225, Atlanta”,
“business_status”: “CLOSED_TEMPORARILY”
},
{
“name”: “Rowdy Tiger Whiskey Bar & Kitchen”,
“type”: [],
“rating”: 3.9,
“reviews”: 338,
“foot_traffic”: 471,
“distance”: 0.16,
“vicinity”: “866 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “topitofffun”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 248,
“distance”: 0.16,
“vicinity”: “756 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “SmoQ’n Hot Grill”,
“type”: [],
“rating”: 4.7,
“reviews”: 143,
“foot_traffic”: 230,
“distance”: 0.16,
“vicinity”: “756 West Peachtree Street Northwest, Atlanta”,
“business_status”: “CLOSED_TEMPORARILY”
},
{
“name”: “Humble Mumble”,
“type”: [],
“rating”: 4.4,
“reviews”: 45,
“foot_traffic”: 278,
“distance”: 0.16,
“vicinity”: “756 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Costa Coffee - Atlanta Midtown”,
“type”: [],
“rating”: 4.2,
“reviews”: 37,
“foot_traffic”: 156,
“distance”: 0.17,
“vicinity”: “CODA Building, 756 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Tiff’s Treats Cookie Delivery”,
“type”: [],
“rating”: 4.4,
“reviews”: 208,
“foot_traffic”: 198,
“distance”: 0.17,
“vicinity”: “Square on Fifth, 848 Spring Street Northwest Ste B, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Daydreamer Coffee”,
“type”: [],
“rating”: 4.2,
“reviews”: 96,
“foot_traffic”: 264,
“distance”: 0.17,
“vicinity”: “859 Spring Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Bro-Ritos”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 251,
“distance”: 0.17,
“vicinity”: “756 West Peachtree Street Northwest Ste. D, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Cypress Street Pint & Plate”,
“type”: [],
“rating”: 4.5,
“reviews”: 3421,
“foot_traffic”: 592,
“distance”: 0.17,
“vicinity”: “817 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Poke Burri”,
“type”: [],
“rating”: 4.1,
“reviews”: 209,
“foot_traffic”: 649,
“distance”: 0.17,
“vicinity”: “756 West Peachtree Street Northwest Suite H, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “KSV JEWERY”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 384,
“distance”: 0.2,
“vicinity”: “848 Spring Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Apotheos Coffee Midtown”,
“type”: [],
“rating”: 4.8,
“reviews”: 95,
“foot_traffic”: 691,
“distance”: 0.2,
“vicinity”: “740 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Moge tee & Korean Style Chicken”,
“type”: [],
“rating”: 4.4,
“reviews”: 30,
“foot_traffic”: 373,
“distance”: 0.2,
“vicinity”: “848 Spring Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Moe’s Southwest Grill”,
“type”: [],
“rating”: 4,
“reviews”: 723,
“foot_traffic”: 488,
“distance”: 0.2,
“vicinity”: “85 5th Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Zoe Tacos”,
“type”: [],
“rating”: 4.8,
“reviews”: 6,
“foot_traffic”: 450,
“distance”: 0.2,
“vicinity”: “75 5th Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Cargoatlanta”,
“type”: [],
“rating”: 4.7,
“reviews”: 14,
“foot_traffic”: 331,
“distance”: 0.21,
“vicinity”: “800 Peachtree Street Northeast, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Starbucks”,
“type”: [],
“rating”: 4,
“reviews”: 379,
“foot_traffic”: 368,
“distance”: 0.22,
“vicinity”: “708 Spring Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Cricket Wireless Authorized Retailer”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 314,
“distance”: 0.28,
“vicinity”: “754 Peachtree Street Northeast, Atlanta”,
“business_status”: “CLOSED_TEMPORARILY”
},
{
“name”: “Einstein Bros. Bagels”,
“type”: [],
“rating”: 3.9,
“reviews”: 561,
“foot_traffic”: 576,
“distance”: 0.28,
“vicinity”: “800 Peachtree Street Northeast, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “European Wax Center”,
“type”: [],
“rating”: 4.9,
“reviews”: 145,
“foot_traffic”: 107,
“distance”: 0.28,
“vicinity”: “800 Peachtree Street Northeast D, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “BenchMark Physical Therapy”,
“type”: [],
“rating”: 4.6,
“reviews”: 42,
“foot_traffic”: 161,
“distance”: 0.28,
“vicinity”: “800 Peachtree Street Northeast E2, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Big Peach Ride + Run - Midtown”,
“type”: [],
“rating”: 4.7,
“reviews”: 281,
“foot_traffic”: 317,
“distance”: 0.29,
“vicinity”: “800 Peachtree Street Northeast suite b&c, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Great American Bacon Race Packet Pick up”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 105,
“distance”: 0.29,
“vicinity”: “800E Peachtree Street Northeast, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Indigo Spring: Atlanta019s Premium Alkaline Spring Water Delivery Service”,
“type”: [],
“rating”: 4.8,
“reviews”: 49,
“foot_traffic”: 180,
“distance”: 0.3,
“vicinity”: “730 Peachtree Street Northeast, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Jackson Edgar N MD”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 336,
“distance”: 0.31,
“vicinity”: “21 8th Street Northeast, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Dr. Michael C. Mclarnon, MD”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 146,
“distance”: 0.34,
“vicinity”: “849 Peachtree Street Northeast, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “S2 Telehealth Technologies”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 125,
“distance”: 0.35,
“vicinity”: “915 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Benjamin Fernando, MD”,
“type”: [],
“rating”: 2,
“reviews”: 3,
“foot_traffic”: 193,
“distance”: 0.35,
“vicinity”: “805 Peachtree Street Northeast Suite A, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “AllCare Primary & Immediate Care”,
“type”: [],
“rating”: 4.6,
“reviews”: 1033,
“foot_traffic”: 420,
“distance”: 0.35,
“vicinity”: “805 Peachtree Street Northeast Suite A, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Strayhorn Gregory MD”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 105,
“distance”: 0.36,
“vicinity”: “805 Peachtree Street Northeast, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Mindwaves Mental Health”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 70,
“distance”: 0.38,
“vicinity”: “855 Peachtree Street Northeast UNIT 3401, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Dr. Olakunle Ajibola”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 353,
“distance”: 0.39,
“vicinity”: “688 Spring Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Brownlee Shaun L MD”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 336,
“distance”: 0.39,
“vicinity”: “688 Spring Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Wainstein Jeffrey T MD”,
“type”: [],
“rating”: 5,
“reviews”: 1,
“foot_traffic”: 171,
“distance”: 0.39,
“vicinity”: “688 Spring Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Physio - Atlanta - Midtown”,
“type”: [],
“rating”: 4.8,
“reviews”: 125,
“foot_traffic”: 160,
“distance”: 0.39,
“vicinity”: “855 Peachtree Street Northeast Suite 1B, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Payton Sheila MD”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 258,
“distance”: 0.43,
“vicinity”: “Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Dr. Malaika E. Berkeley”,
“type”: [],
“rating”: 3.1,
“reviews”: 11,
“foot_traffic”: 417,
“distance”: 0.43,
“vicinity”: “814 Juniper Street Northeast, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “le Denteorgia Dental Implant Center”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 238,
“distance”: 0.44,
“vicinity”: “900 Peachtree Street Northeast, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Famil”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 69,
“distance”: 0.45,
“vicinity”: “675 West Peachtree Street Northwest, Atlanta”,
“business_status”: “OPERATIONAL”
},
{
“name”: “Dr. Mossud M. Smith, DDS”,
“type”: [],
“rating”: null,
“reviews”: null,
“foot_traffic”: 344,
“distance”: 0.48,
“vicinity”: “763 Juniper Street Northeast, Atlanta”,
“business_status”: “OPERATIONAL”
}
],
“image_directory”: “/Users/dhruvnarang/Desktop/hacklytics/pictures/location_20250222_141851_20250222_141857”
}