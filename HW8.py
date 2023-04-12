# Your name: Madison Jennings
# Your student id: 4898 0758
# Your email: maddjenn @umich.edu
# List who you have worked with on this homework:  faye stover

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest


def load_rest_data(db):
    """
    This function accepts the filename of a database as a parameter and returns a
    nested dictionary. Each outer key of the dictionary is the name of each restaurant in
    the database, and each inner key is a dictionary, where the key:value pairs should be the
    category, building, and rating for the restaurant.
    """

    rest_data = {}
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("SELECT * FROM restaurants;")

    for row in c.fetchall():
        
        name = row[1]
        category_id = row[2]
        building_id = row[3]
        rating = row[4]

        c.execute("SELECT category FROM categories WHERE id = ? ", (category_id,))
        category_name = c.fetchone()[0]

        c.execute("SELECT building FROM buildings WHERE id = ?", (building_id,))
        building_num = c.fetchone()[0]

        rest_data[name] = {'category': category_name, 'building': building_num, 'rating': rating}

    conn.close()
    
    return rest_data



def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a
    dictionary. The keys should be the restaurant categories and the values should be
    the number of restaurants in each category. The function should also create a bar
    chart with restaurant categories and the count of number of restaurants in each
    category.
    """
    
    conn = sqlite3.connect(db)
    c = conn.cursor()
    
    # hint: use the SQL COUNT keyword
    c.execute("""
        SELECT categories.category, COUNT(restaurants.id) AS count
        FROM categories
        JOIN restaurants ON categories.id = restaurants.category_id
        GROUP BY categories.category
        ORDER BY count DESC
    """)
    
    categories = dict(c.fetchall())
    conn.close()

    # make bar chart
    fig, ax = plt.subplots()
    ax.barh(list(categories.keys()), list(categories.values()))
    ax.set_xlabel('Number of Restaurants')
    ax.set_ylabel('Restaurant Categories')
    ax.set_title('Type of Restaurant on South University Ave')
    plt.show()
    
    return categories



def find_rest_in_building(building_num, db_filename):
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    c.execute('''SELECT r.name
                 FROM restaurants AS r
                 JOIN buildings AS b
                 ON r.building_id = b.id
                 WHERE b.building = ?
                 ORDER BY r.rating DESC''', (building_num,))
    results = c.fetchall()
    conn.close()
    return [r[0] for r in results]



def get_highest_rating(db):
    """
    This function returns a list of two tuples. The first tuple contains the
    highest-rated restaurant category
    and the average rating of the restaurants in that category, and the second
    tuple contains the building number
    which has the highest rating of restaurants and its average rating.
    This function should also plot two barcharts in one figure. The first bar chart
    displays the categories
    along the y-axis and their ratings along the x-axis in descending order (by
    rating).
    The second bar chart displays the buildings along the y-axis and their ratings
    along the x-axis
    in descending order (by rating).
    """
    
    conn = sqlite3.connect(db)
    c = conn.cursor()

    # Query to get the highest rated category
    category_query = '''
    SELECT categories.category, ROUND(AVG(restaurants.rating), 1)
    FROM categories
    JOIN restaurants ON categories.id = restaurants.category_id
    GROUP BY categories.category
    ORDER BY AVG(restaurants.rating) DESC;
    '''

    # Query to get the highest rated building
    building_query = '''
    SELECT buildings.building, ROUND(AVG(restaurants.rating), 1)
    FROM buildings
    JOIN restaurants ON buildings.id = restaurants.building_id
    GROUP BY buildings.building
    ORDER BY AVG(restaurants.rating) DESC;
    '''

    # Execute the queries and get the results
    c.execute(category_query)
    highest_category = c.fetchone()
    c.execute(building_query)
    highest_building = c.fetchone()

    # Plot the bar charts
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 8))

    # categories
    ax1.set_title('Average Restaurant Ratings by Category')
    ax1.set_xlabel('Rating')
    ax1.set_ylabel('Categories')
    ax1.set_xlim([0, 5])
    c.execute(category_query)
    results = c.fetchall()
    categories = [row[0] for row in results]
    avg_ratings = [row[1] for row in results]
    y_pos = range(len(categories))
    ax1.barh(y_pos, avg_ratings, align='center')
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(categories)

    # buildings
    ax2.set_title('Average Restaurant Ratings by Building')
    ax2.set_xlabel('Ratings')
    ax2.set_ylabel('Buildings')
    ax2.set_xlim([0, 5])
    c.execute(building_query)
    results = c.fetchall()
    buildings = [row[0] for row in results]
    avg_ratings = [row[1] for row in results]
    y_pos = range(len(buildings))
    ax2.barh(y_pos, avg_ratings, align='center')
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(buildings)
    
    plt.show()
    conn.close()
    return [(highest_category[0], highest_category[1]), (highest_building[0], highest_building[1])]


#Try calling your functions here
def main():
    db = 'South_U_Restaurants.db'

class TestHW8(unittest.TestCase):
    
    def setUp(self):
        self.rest_dict = {
        'category': 'Cafe',
        'building': 1101,
        'rating': 3.8
        }
        self.cat_dict = {
        'Asian Cuisine ': 2,
        'Bar': 4,
        'Bubble Tea Shop': 2,
        'Cafe': 3,
        'Cookie Shop': 1,
        'Deli': 1,
        'Japanese Restaurant': 1,
        'Juice Shop': 1,
        'Korean Restaurant': 2,
        'Mediterranean Restaurant': 1,
        'Mexican Restaurant': 2,
        'Pizzeria': 2,
        'Sandwich Shop': 2,
        'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]
    
    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')
    
    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)
        
if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
