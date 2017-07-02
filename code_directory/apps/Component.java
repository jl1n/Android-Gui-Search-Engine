package apps;

import java.util.*; 

//stores information about components found in XML files of apps
public class Component {

	private LinkedHashMap<String, String> attributeMap;
	private int componentId;
	private String componentName;
	private static int componentInstance;
    private int screenId;
	private int parentId;
    private String text;
	private int num_occurrences;	

	public Component() {
		attributeMap = new LinkedHashMap<String, String>(); 
		componentInstance++;
		componentId = componentInstance;
	}

	public void addAttribute(String key, String value) {
		attributeMap.put(key, value);
	}

	public LinkedHashMap<String, String> getAttributeMap() {
		return attributeMap;
	}

	public String getComponentName() {
		return componentName;  
	}

	public int getComponentId() {
		return componentId;
	}

	public void setComponentName(String componentName) {
		this.componentName = componentName;  
	}

	public void setScreenId(int screenId) {
		this.screenId = screenId;
	}

	public int getParentId() {
		return parentId;
	}

	public void setParentId(int parentId) {
		this.parentId = parentId;
	}
}