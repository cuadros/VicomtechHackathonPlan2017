package org.vicomtech.nlp.hackathon.model;

import java.util.Date;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import com.fasterxml.jackson.annotation.JsonProperty;

@Document(collection = "events")
public class KulturalEvent {

	@Id
	private String id;
	@JsonProperty("eventName")
	private String eventName;
	@JsonProperty("startDate")
	private Date startDate;
	@JsonProperty("endDate")
	private Date endDate;
	@JsonProperty("municipality")
	private String municipality;
	@JsonProperty("eventType")
	private String eventType;
	// @JsonProperty("geolocation")
	// private Geolocation geolocation;
	private double latitude;
	private double longitude;

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public String getEventName() {
		return eventName;
	}

	public void setEventName(String eventName) {
		this.eventName = eventName;
	}

	public Date getStartDate() {
		return startDate;
	}

	public void setStartDate(Date startDate) {
		this.startDate = startDate;
	}

	public Date getEndDate() {
		return endDate;
	}

	public void setEndDate(Date endDate) {
		this.endDate = endDate;
	}

	public double getLatitude() {
		return latitude;
	}

	public void setLatitude(double latitude) {
		this.latitude = latitude;
	}

	public double getLongitude() {
		return longitude;
	}

	public void setLongitude(double longitude) {
		this.longitude = longitude;
	}

	public String getMunicipality() {
		return municipality;
	}

	public void setMunicipality(String municipality) {
		this.municipality = municipality;
	}

	public String getEventType() {
		return eventType;
	}

	public void setEventType(String eventType) {
		this.eventType = eventType;
	}

	@Override
	public String toString() {
		return "KulturalEvent [id=" + id + ", eventName=" + eventName + ", startDate=" + startDate + ", endDate="
				+ endDate + ", municipality=" + municipality + ", eventType=" + eventType + ", latitude=" + latitude
				+ ", longitude=" + longitude + "]";
	}

	//
	// public static class Geolocation {
	//
	// @JsonProperty("lat")
	// private double latitude;
	// @JsonProperty("long")
	// private double longitude;
	//
	// public double getLatitude() {
	// return latitude;
	// }
	//
	// public void setLatitude(double latitude) {
	// this.latitude = latitude;
	// }
	//
	// public double getLongitude() {
	// return longitude;
	// }
	//
	// public void setLongitude(double longitude) {
	// this.longitude = longitude;
	// }
	//
	// @Override
	// public String toString() {
	// return "GeoLocation [latitude=" + latitude + ", longitude=" + longitude +
	// "]";
	// }
	//
	//
	//
	// }


}

/*
 * 
 * 
 * 
 * "documentName" :
 * "\"Nynhá Aba. Corazón de indio\", exposición de Ángela Berlinde",
 * "eventCountry" : "108", "eventEndDate" : "30/03/2017", "eventLanguages" :
 * "Gaztelania", "eventRegistrationEndDate" : "05/01/2017",
 * "eventRegistrationStartDate" : "04/01/2017", "eventStartDate" : "13/01/2017",
 * "eventTerritory" : "48", "eventTown" : "020", "eventType" : "Exposición",
 * "latitudelongitude" : "43.2637687790786,-2.93094635009765", "latwgs84" :
 * "43.2637687790786", "lonwgs84" : "-2.93094635009765", "countrycode" : "108",
 * "country" : "España", "territorycode" : "48", "territory" : "Bizkaia",
 * "municipalitycode" : "020", "municipality" : "Bilbao", "placename" :
 * "Centro de Fotografía Contemporánea", "friendlyUrl" :
 * "http://opendata.euskadi.eus/catalogo/-/evento/2017010410154615/nynha-aba-corazon-de-indio-exposicion-de-angela-berlinde/kulturklik/es/",
 * "physicalUrl" :
 * "http://opendata.euskadi.eus/catalogo/contenidos/evento/2017010410154615/es_def/index.shtml",
 * "dataXML" :
 * "http://opendata.euskadi.eus/contenidos/evento/2017010410154615/es_def/data/es_r01dtpd15968c34ae8196db31cd7b6a295b1f75588",
 * "metadataXML" :
 * "http://opendata.euskadi.eus/contenidos/evento/2017010410154615/r01Index/2017010410154615-idxContent.xml",
 * "zipFile" :
 * "http://opendata.euskadi.eus/contenidos/evento/2017010410154615/opendata/2017010410154615.zip"
 * 
 */
