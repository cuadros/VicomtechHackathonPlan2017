package org.vicomtech.nlp.hackathon.database.kulturEvents;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.List;
import java.util.Map;

import org.apache.commons.io.FileUtils;
import org.bson.Document;
//import org.vicomtech.nlp.hackathon.model.KulturalEvent;

import com.google.common.collect.Maps;
import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

public class LoadKulturklikCSVIntoMongoDB {

	
	private static final String CSV_FILE = "kulturklik.csv";
	static MongoClient mongoClient = new MongoClient( "localhost" );
	
	private static DateFormat DATE_FORMAT = new SimpleDateFormat("dd/MM/yyyy");
	
	public static void main(String[] args) {
		
		MongoDatabase db = mongoClient.getDatabase("kulturklik");
		MongoCollection<Document> collection = db.getCollection("events");
		
		List<String> lines = readLines(CSV_FILE);
		//skip first line
		for(String line:lines.subList(1, lines.size())){
			System.out.println("Storing info for line... ");
			Document document = parseLineToDocument(line);
			collection.insertOne(document);
		}
		
		
		
		
	}
	
//	private KulturalEvent parseLineToEvent(String line){
//		String[]parts=line.split(";");
//		KulturalEvent kulturalEvent=new KulturalEvent();
//		kulturalEvent.setDocumentName(parts[0]);
//		return kulturalEvent;
//	}
	
	private static Document parseLineToDocument(String line){
		try{
			String[]parts=line.split(";");
			Document document=new Document();
			document.put("eventName", parts[0]);
			document.put("startDate", DATE_FORMAT.parse(parts[4]));
			document.put("endDate", DATE_FORMAT.parse(parts[2]));
			document.put("eventType", parts[12]);
			document.put("municipality", parts[21]);
			document.put("urlAmigable", parts[23]);
			Map<String,Double> loc = Maps.newHashMap();
			loc.put("lat", Double.parseDouble(parts[14]));
			loc.put("long", Double.parseDouble(parts[15]));
			document.put("geolocation",loc); //new Double[]{Double.parseDouble(parts[14]),Double.parseDouble(parts[15])});
			document.put("latitude",Double.parseDouble(parts[14]));
			document.put("longitude",Double.parseDouble(parts[15]));
			
			return document;
		}catch(Exception e){
			throw new RuntimeException(e);
		}
	}
	
	
	
	private static List<String>readLines(String path){
		try {
			return FileUtils.readLines(new File(path),StandardCharsets.UTF_8);
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}
	
	
}
