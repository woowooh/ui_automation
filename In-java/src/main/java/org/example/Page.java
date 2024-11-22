package org.example;


import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.interactions.Actions;


public abstract class Page {
    WebDriver driver = new ChromeDriver();

    public abstract void run() throws InterruptedException;

    public abstract void beforeRun();

    public void main() throws InterruptedException {
        this.beforeRun();
        this.run();
        this.afterRun();
    }

    public void afterRun() {
        this.driver.quit();
    }

    public void input(String cssTag, String value) {
        WebElement inputElement = driver.findElement(By.cssSelector(cssTag));
        inputElement.sendKeys(value);
    }

    public void click(String cssTag) {
        WebElement buttonElement = driver.findElement(By.cssSelector(cssTag));
        buttonElement.click();
    }

    public void typeEnter(String cssTag) {
        WebElement element = driver.findElement(By.cssSelector(cssTag));
        element.sendKeys(Keys.ENTER);
    }

    public void keyboardEnter() {
        Actions actions = new Actions(driver);
        actions.sendKeys(Keys.RETURN).perform();
    }
}
