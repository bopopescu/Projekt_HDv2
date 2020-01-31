containers = set()
brand = ""
product_name = ""
shipping = ""
brand = []
product_name = []
shipping = []


def switch_case():
@@ -52,18 +52,18 @@ def switch_case():
    elif input_choice == 2:
        try:
            # get info for each product
            for container in containers:
            for index, container in enumerate(containers, start=0):
                brand_container = container.findAll("div", {"class": "item-info"})
                brand = brand_container[0].div.a.img["title"]
                brand.append(brand_container[0].div.a.img["title"])

                title_container = container.findAll("a", {"class": "item-title"})
                product_name = title_container[0].text
                product_name.append(title_container[0].text)

                shipping_container = container.findAll("li", {"class": "price-ship"})
                shipping = shipping_container[0].text.strip()
                shipping.append(shipping_container[0].text.strip())

            # ask for continue
            input_continue = input('want to continue Y/N?: ')
            input_continue = input('want to continue Y/N?: ').upper()
            if input_continue == 'Y':
                switch_case()
        except NameError:
@@ -88,22 +88,101 @@ def switch_case():
                           "shipping varchar(255)"
                           ");")

            cursor.execute("INSERT INTO etl (brand, product_name, shipping) VALUES (%s,%s,%s)",
                           (brand, product_name.replace(",", "|"), shipping))
            mariadb_connection.commit()
            for index, container in enumerate(containers, start=0):
                cursor.execute("INSERT INTO etl (brand, product_name, shipping) VALUES (%s,%s,%s)",
                               (brand[index], product_name[index].replace(",", "|"), shipping[index]))
                mariadb_connection.commit()

            brand.clear()
            product_name.clear()
            shipping.clear()

            # ask for continue
            input_continue = input('want to continue Y/N?: ')
            input_continue = input('want to continue Y/N?: ').upper()
            if input_continue == 'Y':
                switch_case()
        except NameError:
            print('First u need to run step 1 and step 2.')
            switch_case()

    # do all etl
    elif input_choice == 4:
        # open connection
        u_client = uReq(my_url)
        page_html = u_client.read()
        u_client.close()

        # html parsing
        page_soup = soup(page_html, "html.parser")

        # grabs each product
        containers = page_soup.find_all("div", {"class": "item-container"})

        # open config file and assign variables
        config = configparser.ConfigParser()
        config.read("config.ini")
        db = config['mysql']['db']
        db_user = config['mysql']['user']
        db_password = config['mysql']['password']

        # connect to MariaDB
        mariadb_connection = mariadb.connect(user=db_user, password=db_password, database=db)
        cursor = mariadb_connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS etl ("
                       "brand varchar(225),"
                       "product_name varchar(225),"
                       "shipping varchar(255)"
                       ");")

        # get info for each product
        for index, container in enumerate(containers, start=0):
            brand_container = container.findAll("div", {"class": "item-info"})
            brand.append(brand_container[0].div.a.img["title"])

            title_container = container.findAll("a", {"class": "item-title"})
            product_name.append(title_container[0].text)

            shipping_container = container.findAll("li", {"class": "price-ship"})
            shipping.append(shipping_container[0].text.strip())

        for index, container in enumerate(containers, start=0):
            cursor.execute("INSERT INTO etl (brand, product_name, shipping) VALUES (%s,%s,%s)",
                           (brand[index], product_name[index].replace(",", "|"), shipping[index]))
            mariadb_connection.commit()

        brand.clear()
        product_name.clear()
        shipping.clear()

        # ask for continue
        input_continue = input('want to continue Y/N?: ').upper()
        if input_continue == 'Y':
            switch_case()

    elif input_choice == 5:
        # erase data

        # open config file and assign variables
        config = configparser.ConfigParser()
        config.read("config.ini")
        db = config['mysql']['db']
        db_user = config['mysql']['user']
        db_password = config['mysql']['password']

        # connect to MariaDB
        mariadb_connection = mariadb.connect(user=db_user, password=db_password, database=db)
        cursor = mariadb_connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS etl;")
        mariadb_connection.commit()
        print('data erased.')

        # ask for continue
        input_continue = input('want to continue Y/N?: ').upper()
        if input_continue == 'Y':
            switch_case()

    else:
        print('U can only choose from options 1 to 5.')