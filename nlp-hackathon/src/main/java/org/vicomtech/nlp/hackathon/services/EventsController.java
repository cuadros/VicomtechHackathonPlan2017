package org.vicomtech.nlp.hackathon.services;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.vicomtech.nlp.hackathon.database.hotels.HotelsRepository;
import org.vicomtech.nlp.hackathon.database.kulturEvents.EventsRepository;
import org.vicomtech.nlp.hackathon.database.restaurants.RestaurantsRepository;
import org.vicomtech.nlp.hackathon.model.Hotel;
import org.vicomtech.nlp.hackathon.model.KulturalEvent;
import org.vicomtech.nlp.hackathon.model.Restaurant;


@Controller
public class EventsController {

	private static final Logger LOGGER=LoggerFactory.getLogger(EventsController.class);

	
	@Autowired
	private EventsRepository eventsRepository;
	@Autowired
	private HotelsRepository hotelsRepository;
	@Autowired
	private RestaurantsRepository restaurantsRepository;
	
	@CrossOrigin()
	@RequestMapping(value="/events",method={RequestMethod.GET})
	public @ResponseBody List<KulturalEvent> getAllKulturalEvents(
			@RequestParam(name="municipality", required=false)String municipality,
			@RequestParam(name="type", required=false)String eventType,
			@RequestParam(name="date", required=false)String dateStr
			){
		LOGGER.info("Receiving call with params, municipality={}, type={} and date={}",municipality,eventType,dateStr);
		return eventsRepository.findByCriteria(municipality, eventType, dateStr);

	}
	
	@CrossOrigin()
	@RequestMapping(value="/hotels",method={RequestMethod.GET})
	public @ResponseBody List<Hotel> getHotels(@RequestParam(name="municipality", required=false)String municipality){
		LOGGER.info("Receiving call with params, municipality={}",municipality);
		return hotelsRepository.findByCriteria(municipality);
	}
	
	@CrossOrigin()
	@RequestMapping(value="/restaurants",method={RequestMethod.GET})
	public @ResponseBody List<Restaurant> getRestaurants(@RequestParam(name="municipality", required=false)String municipality){
		LOGGER.info("Receiving call with params, municipality={}",municipality);
		return restaurantsRepository.findByCriteria(municipality);
	}
	
}
