package org.vicomtech.nlp.hackathon.database.restaurants;

import java.util.List;
import java.util.regex.Pattern;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.vicomtech.nlp.hackathon.database.hotels.HotelsRepositoryImpl;
import org.vicomtech.nlp.hackathon.model.Restaurant;

public class RestaurantsRepositoryImpl implements RestaurantsRepositoryCustom{

	private static final Logger LOGGER=LoggerFactory.getLogger(HotelsRepositoryImpl.class);
	
	@Autowired
	MongoTemplate mongoTemplate;
	
	@Override
	public List<Restaurant> findByCriteria(String municipality) {
		String dbName = mongoTemplate.getDb().getName();
		LOGGER.info("Querying to database: {} for hotels with municipality:{}", dbName,municipality);
		Query query = new Query();
		if(municipality!=null){
			query.addCriteria(Criteria.where("municipality")
				.regex(Pattern.compile(Pattern.quote(municipality), Pattern.CASE_INSENSITIVE)));
		}		
		return mongoTemplate.find(query, Restaurant.class);
	}
	
}
