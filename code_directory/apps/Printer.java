package apps;

import org.xml.sax.SAXParseException;
import java.util.*;
import java.io.*;

public class Printer {

	public static void printCSV(List<Application> appList, HashMap<String, Integer> whatever) {
		try {
			//erases previous csv data
			PrintWriter eraseApplication = new PrintWriter("application.csv");
			eraseApplication.print("");
			eraseApplication.close();

			eraseApplication = new PrintWriter("file.csv");
			eraseApplication.print("");
			eraseApplication.close();

			eraseApplication = new PrintWriter("component.csv");
			eraseApplication.print("");
			eraseApplication.close();

			eraseApplication = new PrintWriter("attributes.csv");
			eraseApplication.print("");
			eraseApplication.close();


			Writer applicationWriter = new FileWriter("application.csv", true);
			Writer screenWriter = new FileWriter("file.csv", true);
			Writer componentWriter = new FileWriter("component.csv", true);
			Writer something = new FileWriter("attributes.csv", true);
			String text = "";

				//print application info
			for (Application applicationEntry : appList) {
				text += Integer.toString(applicationEntry.getAppId());
				text += ',';
				text += applicationEntry.getAppName();
				text += "\n";
				applicationWriter.append(text);
				text = "";

					//print file info
				for(Screen screenEntry : applicationEntry.getScreenList()) {
					text += Integer.toString(screenEntry.getScreenId());
					text += ',';
					text += screenEntry.getAppId();
					text += ',';
					text += screenEntry.getScreenName();
					text += ',';
					for (Map.Entry<String, Integer> entry : screenEntry.getComponentCount().entrySet()) {
						text+=entry.getKey();
						text += ':';
						text += Integer.toString(entry.getValue());
						text += ' ';
					}
					text += ',';
					text += "\"";
					text += screenEntry.getScreenXML().replaceAll("\n","~`").replaceAll(",","%@");
					text += "\"";
					text += "\n";
					screenWriter.append(text);
					text = "";

						//print component info
					for(Component componentEntry : screenEntry.getComponentList()) {
						text += Integer.toString(componentEntry.getComponentId());
						text += ',';
						text += screenEntry.getScreenId();
						text += ',';
						text += componentEntry.getParentId();
						text += ',';
						text += componentEntry.getComponentName();
						text += ',';
						text += componentEntry.getAttributeMap().get("android:id");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:src");
						text += ',';
						text += componentEntry.getAttributeMap().get("xmlns:android");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:orientation");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:layout_height");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:layout_width");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:layout_weight");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:layout_gravity");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:gravity");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:layout_margin");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:layout_marginLeft");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:layout_marginTop");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:layout_marginRight");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:layout_marginBottom");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:padding");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:paddingLeft");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:paddingTop");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:paddingRight");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:paddingBottom");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:clickable");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:text");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:textColor");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:textSize");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:textStyle");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:textAppearance");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:color");
						text += ',';
						text += componentEntry.getAttributeMap().get("android:background");
						text += ',';
						text += "0";
						text += "\n";
						componentWriter.append(text);
						text = "";
					}
				}
				text = "";
			}

			//print attribute totals
			Map<String, Integer> map = sortByValues(whatever); 

			text = "";
			for(Map.Entry<String, Integer> entry : map.entrySet()){
				text += entry.getKey();
				text += ",";
				text += Integer.toString(entry.getValue());
				text += "\n";
				something.append(text);
				text = "";
			}

			screenWriter.close();
			applicationWriter.close();
			componentWriter.close();
			something.close();

		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}

		//sorts hashmap by value
	private static HashMap sortByValues(HashMap map) { 
		List list = new LinkedList(map.entrySet());
		// Defined Custom Comparator here
		Collections.sort(list, new Comparator() {
			public int compare(Object o1, Object o2) {
				return ((Comparable) ((Map.Entry) (o1)).getValue())
				.compareTo(((Map.Entry) (o2)).getValue());
			}
		});
		
		// Here I am copying the sorted list in HashMap
		// using LinkedHashMap to preserve the insertion order
		HashMap sortedHashMap = new LinkedHashMap();
		for (Iterator it = list.iterator(); it.hasNext();) {
			Map.Entry entry = (Map.Entry) it.next();
			sortedHashMap.put(entry.getKey(), entry.getValue());
		} 
		return sortedHashMap;
	}

}