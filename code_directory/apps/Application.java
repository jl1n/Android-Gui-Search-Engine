package apps;

import java.util.*; 

//Stores information about apps parsed through
public class Application {

	private ArrayList<Screen> screenList;
	private static int appInstance = 0;
    private String appName;
	private String repo;
    private String image;
	private int appId;

	public Application() {
	screenList = new ArrayList<Screen>();
	appInstance++;
	appId = appInstance;
	}

	public void addScreen(Screen screen) {
		screenList.add(screen);
	}

	public ArrayList<Screen> getScreenList() {
		return screenList;
	}

	public int getAppId() {
		return appId;
	}
	public void setAppId(int appId) {
		this.appId = appId;
	}

	public String getAppName() {
		return appName;
	}
	public void setAppName(String appName) {
		this.appName = appName;
	}

}