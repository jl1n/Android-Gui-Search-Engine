import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;


public class CsvFileWriter{
    
    private static final String COMMA_DELIMITER = ",";
    private static final String NEW_LINE_SEPARATOR = "\n";

    public static void writeCsv(String filename){
        
        // Create new XML document objects

        // Create a list of those document objects



        try{
            fileWriter = new FileWriter(fileName);

            //Write CSV File header
            fileWriter.append(FILE_HEADER.toString());

            fileWriter.append(NEW_LINE_SEPARATOR);

            // for each attribute for each XML file, add it to the CSV list
        }

        catch (IOException e){
            System.out.println("Error in CsvFileWriter");
            e.printStackTrace();
        }



    }


}