package org.vicomtech.nlp.hackathon.database;

import java.io.IOException;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.regex.Pattern;

import org.bson.BsonDocument;
import org.bson.Document;
import org.bson.conversions.Bson;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.google.common.collect.Lists;
import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;

public class CheckQueries {

	static MongoClient mongoClient = new MongoClient( "localhost" );
	
	static DateFormat DATE_FORMAT=new SimpleDateFormat("dd/MM/yyyy");
	
	public static void main(String[] args) throws JsonParseException, JsonMappingException, IOException, ParseException {
		// TODO Auto-generated method stub

		MongoDatabase db = mongoClient.getDatabase("kulturklik");
		MongoCollection<Document> collection = db.getCollection("events");
		
		//MongoCursor<Document> events = collection.find().iterator();
		
		Bson filter = Filters.eq("eventType", "Concierto");
		filter=Filters.or(filter,Filters.eq("eventType","Teatro"));
		
		filter=Filters.and(filter,Filters.regex("municipality",Pattern.compile(Pattern.quote("bilbao"), Pattern.CASE_INSENSITIVE)));
		
		String DATES="25/06/2017,26/03/2017";
		String[]split=DATES.split(",");
		
		Bson datesFilter=Filters.exists("startDate");
		List<Bson>dateFilters=Lists.newArrayList();
		for(String dateStr:split){
			System.err.println("Adding filters for date: "+dateStr);
			Date date=DATE_FORMAT.parse(dateStr);
			dateFilters.add(Filters.and(Filters.gte("endDate", date),Filters.lte("startDate", date)));
		}
		
		datesFilter=Filters.or(dateFilters);
		filter=Filters.and(filter,datesFilter);
		
		System.out.println(filter.toString());
		System.out.println(filter.toBsonDocument(BsonDocument.class, MongoClient.getDefaultCodecRegistry()));
		
		MongoCursor<Document> events =collection.find(filter).iterator();
		
		int count=0;
		
		while(events.hasNext()){
			Document event = events.next();
//			ObjectMapper mapper=new ObjectMapper();
//			mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
//			KulturalEvent kevent=mapper.readValue(event.toJson(),KulturalEvent.class);
//			System.out.println(kevent);
			
			System.out.println(event);
			
			count++;
		}
		
		System.out.println("TOTAL RESULTS: "+count);
		
	}

}
