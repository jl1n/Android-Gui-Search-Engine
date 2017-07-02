package apps;

import java.util.*; 

//stores information about individual xml files in layout folder of apps.
public class Screen {
	
	private ArrayList<Component> componentList;
	private LinkedHashMap<String, Integer> componentCount;
	private int appId;
	private int screenId;
	private static int screenInstance = 0;
	private String screenName;
	private String screenXML;

	public Screen() {
		componentList = new ArrayList<Component>();
		componentCount = new LinkedHashMap<String, Integer>(); 
		screenInstance++;
		screenId = screenInstance;
	}

	public LinkedHashMap<String, Integer> getComponentCount() {
		return componentCount;
	}	
	public ArrayList<Component> getComponentList() {
		return componentList;
	}
	
	public void addComponent(Component component) {
		componentList.add(component);
	} 
	
	public int getAppId() {
		return appId;
	}
	public void setAppId(int appId) {
		this.appId = appId;
	}
	
	public String getScreenName() {
		return screenName;
	}
	public void setScreenName(String screenName) {
		this.screenName = screenName;
	}
	
	public int getScreenId() {
		return screenId;
	}

	public String getScreenXML() {
		return screenXML;
	}
	public void setScreenXML(String screenXML) {
		this.screenXML = screenXML;
	}

}