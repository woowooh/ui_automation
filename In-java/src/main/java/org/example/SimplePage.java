package org.example;


public class SimplePage extends Page {
    static final String loginPage = "https://www.12306.cn/index/";

    public void gotToLoginPage() {
        this.driver.get(SimplePage.loginPage);
    }

    public void doLogin() throws InterruptedException {
        String loginTag = "#fromStationText";
        this.click(loginTag);
        this.input(loginTag, "潍坊");
        this.keyboardEnter();
        while (true) {
            Thread.sleep(1000);
        }
    }

    @Override
    public void run() throws InterruptedException {
        this.gotToLoginPage();
        this.doLogin();
    }

    @Override
    public void beforeRun() {

    }

    public static void main(String[] args) throws InterruptedException {
        Page p = new SimplePage();
        p.main();
    }
}
