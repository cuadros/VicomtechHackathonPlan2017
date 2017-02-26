package org.vicomtech.nlp.hackathon.database.kulturEvents;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.regex.Pattern;

import org.bson.BsonDocument;
import org.bson.conversions.Bson;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.BasicQuery;
import org.springframework.data.mongodb.core.query.Query;
import org.vicomtech.nlp.hackathon.model.KulturalEvent;

import com.google.common.collect.Lists;
import com.mongodb.MongoClient;
import com.mongodb.client.model.Filters;

public class EventsRepositoryImpl implements EventsRepositoryCustom {

	private static final Logger LOGGER = LoggerFactory.getLogger(EventsRepositoryImpl.class);
	
	private static DateFormat DATE_FORMAT = new SimpleDateFormat("dd/MM/yyyy");

	@Autowired
	MongoTemplate mongoTemplate;

	@Override
	public List<KulturalEvent> findByCriteria(String municipality, String eventType, String desiredDate) {
		// String dbName = mongoTemplate.getDb().getName();
		// LOGGER.info("Querying to database: {}", dbName);
		//
		// Query query = new Query();
		// if (municipality != null) {
		// query.addCriteria(Criteria.where("municipality")
		// .regex(Pattern.compile(Pattern.quote(municipality),
		// Pattern.CASE_INSENSITIVE)));
		// }
		// if (eventType != null) {
		// query.addCriteria(Criteria.where("eventType")
		// .regex(Pattern.compile(Pattern.quote(eventType),
		// Pattern.CASE_INSENSITIVE)));
		// }
		// if (desiredDate != null) {
		// query.addCriteria(Criteria.where("endDate").gte(desiredDate)
		// .andOperator(Criteria.where("startDate").lte(desiredDate)));
		// }
		// return mongoTemplate.find(query, KulturalEvent.class);
		return findByCriteria2(municipality, eventType, desiredDate);
	}

	private List<KulturalEvent> findByCriteria2(String municipality, String eventType, String desiredDate) {
		String dbName = mongoTemplate.getDb().getName();
		LOGGER.info("Querying to database: {}", dbName);

		if(municipality==null && eventType==null && desiredDate==null){
			return mongoTemplate.findAll(KulturalEvent.class);
		}
		
		List<Bson>allFilters=Lists.newArrayList();
		
		List<Bson> muniFilters = Lists.newArrayList();
		if (municipality != null) {
			String[] munis = municipality.split(",");
			for (String muni : munis) {
				muniFilters.add(
						Filters.regex("municipality", Pattern.compile(Pattern.quote(muni), Pattern.CASE_INSENSITIVE)));
			}
			Bson muniFilter = Filters.or(muniFilters);
			allFilters.add(muniFilter);
		}
		

		List<Bson> typesFilter = Lists.newArrayList();
		if (eventType != null) {
			String[] types = eventType.split(",");
			for (String type : types) {
				typesFilter.add(
						Filters.regex("eventType", Pattern.compile(Pattern.quote(type), Pattern.CASE_INSENSITIVE)));
			}
			Bson typeFilter = Filters.or(typesFilter);
			allFilters.add(typeFilter);
		}
		

		List<Bson> datesFilter = Lists.newArrayList();
		if (desiredDate != null) {
			String[] datesStr = desiredDate.split(",");

			for (String dateStr : datesStr) {
				datesFilter.add(Filters.and(Filters.gte("endDate", formatDate(dateStr)), Filters.lte("startDate", formatDate(dateStr))));
			}
			Bson dateFilter = Filters.or(datesFilter);
			allFilters.add(dateFilter);
		}
		

		Bson finalFilter = Filters.and(allFilters);//);

		System.err.println(finalFilter.toString());
		System.err.println(finalFilter.toBsonDocument(BsonDocument.class, MongoClient.getDefaultCodecRegistry()).toJson());
		Query q=new BasicQuery(finalFilter.toBsonDocument(BsonDocument.class, MongoClient.getDefaultCodecRegistry()).toJson());
		
		return mongoTemplate.find(q, KulturalEvent.class);
	}
	
	private Date formatDate(String dateStr){
		try {
			return DATE_FORMAT.parse(dateStr);
		} catch (ParseException e) {
			throw new RuntimeException(e);
		}
	}

}
