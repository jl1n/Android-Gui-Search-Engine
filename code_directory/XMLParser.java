import org.w3c.dom.*;
import org.xml.sax.SAXParseException;
import javax.xml.parsers.*;
import java.util.*;
import java.io.*;
import apps.*;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class XMLParser {
	
	// Put XML file components into HashMap
	public static void main(String[] args) throws Exception {
		
		//replace path here with path to directory with app folders
		File root = new File("/home/ExampleFilePath");

		//XML file input stream
		DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
		DocumentBuilder builder = factory.newDocumentBuilder();
		
		HashMap<String, Integer> attributeCount = new HashMap<String, Integer>();
		
		//erases previous csv data if any
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
		
		//stores all the application objects	
		List<Application> appList = new ArrayList<Application>();
		try {
			
			File allApps[] = root.listFiles();
			String d;
			File manifest;
			String appName = null;
			Document document; 
			
			//go through each application in specified folder
			for(File app : allApps)	{
				
				
				//find layout folder
				d = findDir(app,"layout");
				
				if( d == null){
					continue;
				}
				
				Application application = new Application();

				//find app name
				//---------------------------------------------------------------------------------------
				manifest = findFile(app,"AndroidManifest.xml");
				appName = null;
				
				if(manifest!=null) {
					try {
					//check manifest for file name, normally in application element
						document = builder.parse(new FileInputStream(manifest));
						NodeList nodeList = document.getElementsByTagName("application");
						if(nodeList!=null && (Element)nodeList.item(0) != null) {
							if(((Element)nodeList.item(0)).getAttribute("android:label") != null){
								String[] parts = ((Element)nodeList.item(0)).getAttribute("android:label").split("/");
								//if stored in values, check there
								if(parts[0].equals("@string")) {	
									File file = findFile(app,"values");
									File allValues[] = file.listFiles();
									ArrayList<File> xmlValues = new ArrayList<File>();	
									for (File files : allValues) {
										if((files.getName().substring(files.getName().lastIndexOf(".") + 1).equals("xml"))){
											xmlValues.add(files);
										}
									}
									if(file != null){
										//go through string attributes in every xml in values folder
										for(File value : xmlValues)	{
											document = builder.parse(new FileInputStream(value));	
											document.normalize();
											nodeList = document.getElementsByTagName("string");
											for(int i = 0; i < nodeList.getLength(); i++) {

												if(((Element)nodeList.item(i)).getAttribute("name").equals(parts[1])) {
													appName = nodeList.item(i).getFirstChild().getNodeValue();
												}
												if(appName!=null)
													break;
											}
										}
									}
								}
								//if can't find app name use folder name
								else {
									if(!parts[0].equals(""))
										appName = parts[0].trim();
									else
										appName = "(folder name)" + app.getName();
								}
							}	
						}
					}
					catch (SAXParseException e) {
						System.out.println("Invalid XML file entered");
					}
				}

				if(appName == null)
					application.setAppName("(folder name)" + app.getName());
				else if(appName.equals(""))
					application.setAppName("(nothing)" + app.getName());
				else
					application.setAppName(appName.trim());
				//---------------------------------------------------------------------------------------

				File directory = new File(d);
				File files[] = directory.listFiles();
				
				//go through each XML file
				for (File f : files) {
					if(!(f.getName().substring(f.getName().lastIndexOf(".") + 1).equals("xml"))){
						continue;
					}
					
					//create screen object
					Screen screen = new Screen();
					screen.setScreenName(f.getName());
					screen.setAppId(application.getAppId());
					
					//store xml text as string
					String fString = f.toString();
					String content = readFile(fString, Charset.defaultCharset());
					screen.setScreenXML(content);

					try
					{
						document = builder.parse(new FileInputStream(f));
					}
					catch (SAXParseException e) {
						System.out.println("Invalid XML file entered");
						continue;
					}

					Element rootElement = document.getDocumentElement();
					visitComponents(rootElement, 0, screen, attributeCount);
					application.addScreen(screen);

				}
				appList.add(application);
			}
			
			//print to csv file
			Printer.printCSV(appList,attributeCount);
		}
		
		catch (IOException e) {
			e.printStackTrace();
		} 
	}
	// method to convert xml to string
	static String readFile(String f, Charset encoding) 
	throws IOException 
	{
		Path path;
		path = Paths.get(f);
		byte[] encoded = Files.readAllBytes(path);
		return new String(encoded, encoding);
	}
	
	//Finds directory with the given name
	private static String findDir(File root, String dirName)
	{
		if (root.getName().equals(dirName))
			return root.getAbsolutePath();
		
		File[] fileList = root.listFiles();
		
		if(fileList != null)
		{
			for (File f : fileList)  
			{
				if(f.isDirectory())
				{
					String path = findDir(f, dirName);
					if (path == null)
						continue;
					else
						return path;
				}
			}
		}
		return null;
	}
	
	//Finds directory with the given name
	private static File findFile(File root, String fileName)
	{
		if (root.getName().equals(fileName))
			return root;
		
		File[] fileList = root.listFiles();
		
		if(fileList != null)
		{
			for (File f : fileList)  
			{
				File path = findFile(f, fileName);
				if (path == null)
					continue;
				else
					return path;
			}
		}
		return null;
	}
	
	
	// recursively traverses each component of an xml file and stores attribute
	private static void visitComponents(final Node e, int parentId, Screen screen, HashMap attributeCount) {
		final NodeList children = e.getChildNodes();
		Component component = new Component();
		String compName = e.getNodeName();
		LinkedHashMap<String, Integer> compMap = screen.getComponentCount();
		
		//sets component values that aren't attributes
		component.setScreenId(screen.getScreenId());
		component.setParentId(parentId);
		component.setComponentName(compName);
		
		//counts component types per file and stores to screen
		Integer val = (Integer)compMap.get(compName);
		if(val!=null) {
			compMap.put(compName,(Integer)compMap.get(compName) + 1);
		}
		else {
			compMap.put(compName,1);
		}
		
		// store each attribute of the component to hashmap
		NamedNodeMap attributeList = e.getAttributes();	
		for (int a = 0; a < attributeList.getLength(); a++) 
		{
			Node attribute = attributeList.item(a);
			String name = attribute.getNodeName();
			Integer value = (Integer)attributeCount.get(name);
			
			//counts total number of attributes
			if(value != null){
				attributeCount.put(name, (Integer)attributeCount.get(name) + 1);
			}
			else{
				attributeCount.put(name, 1);
			}
			
			//adds the attribute to hashmap
			component.addAttribute(attribute.getNodeName(), attribute.getNodeValue().replaceAll(",",""));
		}
		
		//goes through the children of each component 
		for (int index = 0; index < children.getLength(); index++)
		{
			Node node = children.item(index);
			if (node.getNodeType() == Node.ELEMENT_NODE)
			{		
				visitComponents(node, component.getComponentId(), screen, attributeCount);	
			}
		}
		screen.addComponent(component);
	}
}