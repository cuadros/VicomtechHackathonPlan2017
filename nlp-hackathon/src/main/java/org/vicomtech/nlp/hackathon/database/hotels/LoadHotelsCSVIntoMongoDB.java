package org.vicomtech.nlp.hackathon.database.hotels;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;

import org.apache.commons.io.FileUtils;
import org.bson.Document;

import com.google.common.collect.Lists;
import com.google.common.collect.Maps;
import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

public class LoadHotelsCSVIntoMongoDB {

	
	private static final String CSV_FILE = "alojamientos.csv";
	static MongoClient mongoClient = new MongoClient( "localhost" );
	
	public static void main(String[] args) {
		
		MongoDatabase db = mongoClient.getDatabase("kulturklik");
		MongoCollection<Document> collection = db.getCollection("hotels");
		
		List<String> lines = readLines(CSV_FILE);
		//skip first line
		for(String line:lines.subList(1, lines.size())){
			System.out.println("Storing info for line... ");
			System.out.println(line);
			Document document = parseLineToDocument(line);
			collection.insertOne(document);
		}

	}
	
	private static Document parseLineToDocument(String line){
		try{
		String[]parts=line.split(";");
		Document document=new Document();
		document.put("hotelName", parts[0]);
		document.put("hotelDescription", parts[1]);
		document.put("municipality", parts[18]);
		document.put("stars", parts[7]);
		document.put("web", parts[29]);
		Map<String,Double> loc = Maps.newHashMap();
		loc.put("lat", checkValueOrZero(parts[32]));
		loc.put("long", checkValueOrZero(parts[33]));
		document.put("geolocation",loc);
		document.put("latitude",checkValueOrZero(parts[32]));
		document.put("longitude",checkValueOrZero(parts[33]));
		
		return document;
		}catch(Exception e){
			throw new RuntimeException(e);
		}
	}
	
	private static double checkValueOrZero(String value){
		return value.trim().length()>0?Double.parseDouble(value):0.0;
	}
	
	
	private static List<String>readLines(String path){
		try {
			String allContent=FileUtils.readFileToString(new File(path),StandardCharsets.UTF_8);
			//allContent=allContent.replaceAll("([^\r])\n", "$1 ");
			return Lists.newArrayList(allContent.split("\r\n"));
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}
	
	
}
