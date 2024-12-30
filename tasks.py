from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Tables import Tables

@task

def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(
        # NOTE: `screenshot="only-on-failure"` is the default.
        # If this function finishes with an exception, it will make a screenshot and
        #  embed it into the logs.
        screenshot="only-on-failure",

        # Interactions may be run in slow motion (given in milliseconds).
        slowmo=100
    )

    # website = open_robot_order_website()
    
    orderList = get_orders()
    open_robot_order_website()
    

    for row in orderList:
        close_annoying_modal()
        fill_the_form(row['Head'],row['Body'],row['Legs'],row['Address'])
        submit_order()


def open_robot_order_website():
    """
    Open Robot ordering website
    """
    
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def get_orders():
    """
    Downloads order file
    """

    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)


    orders = Tables()
    ordersList = orders.read_table_from_csv("orders.csv")
    return ordersList

def close_annoying_modal():
    """
    Closes popup when opening robot order page
    """
    page = browser.page()
    page.locator("xpath=//button[contains(.,'OK')]").click()

def fill_the_form(head, body, legs, address):
    """
    Fills out robot creation form
    """
    page = browser.page()
    page.locator("#head").select_option(head)
    #page.locator("xpath=//div["+body+"]/label").click()
    page.locator(".radio:nth-child("+body+") > label").click()
    page.locator("xpath=//label[contains(.,'3. Legs:')]/../input").fill(legs)
    page.locator("#address").fill(address)
    page.locator("#preview").click()

def submit_order():
    """
    Submits order
    """
    page = browser.page()
    page.locator("#order").click()
    #pageExists = page.locator("xpath=//h3[contains(.,'Receipt')]").exists()
    #page.locator(".alert").wait_for()
    #page.locator("xpath=//div[contains(.,'Thank you for your order!')]").wait_for()
    try:
        page.locator("#order-another").click()
        pass
    except BaseException:
        page.locator("#order").click()
        page.locator("#order-another").click()

