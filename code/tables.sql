---------------------------------------------
-- Table to load Daywise Forecast
---------------------------------------------
DROP TYPE IF EXISTS "flagYesNo";

CREATE TYPE "flagYesNo" AS ENUM (
    'Y',
    'N'
);

DROP TABLE IF EXISTS "contentChoice";

CREATE TABLE "contentChoice"
(
	"id"			SERIAL		PRIMARY KEY,
	"locationName"	VARCHAR,
	"shortName"		VARCHAR,
	"city"			VARCHAR,
	"latitude"		NUMERIC,
	"longitude"		NUMERIC,
	"homePage"		"flagYesNo"
);

SELECT * FROM "contentChoice";

INSERT INTO "contentChoice" ("locationName", "shortName", "city", "latitude", "longitude", "homePage")
VALUES('University of California, Los Angeles', 'UCLA', 'Los Angeles', 34.07956, -118.44494, 'Y');

INSERT INTO "contentChoice" ("locationName", "shortName", "city", "latitude", "longitude","homePage")
VALUES('University of California, Berkeley', 'UCB', 'Berkeley', 37.871853, -122.258423, 'N');

INSERT INTO "contentChoice" ("locationName", "shortName", "city", "latitude", "longitude","homePage")
VALUES('University of California, San Diego', 'UCSD', 'La Jolla', 32.87888, -117.23593, 'N');

INSERT INTO "contentChoice" ("locationName", "shortName", "city", "latitude", "longitude","homePage")
VALUES('University of California, Santa Barbara', 'UCSB', 'Santa Barbara', 34.413963, -119.848946, 'N');

INSERT INTO "contentChoice" ("locationName", "shortName", "city", "latitude", "longitude","homePage")
VALUES('University of California, Irvine', 'UCI', 'Irvine', 33.64099, -117.84437, 'N');

SELECT * FROM "contentChoice";

---------------------------------------------
-- Table to load Daywise Forecast
---------------------------------------------
DROP TABLE IF EXISTS "dailyForecastTB";

CREATE TABLE "dailyForecastTB"
(
	"id"	SERIAL		PRIMARY KEY,
	"responseNumber"	INTEGER,
	"responseName"		VARCHAR,
	"city"				VARCHAR,
	"latitude"			NUMERIC,
	"longitude"			NUMERIC,
	"startDateTime"		TIMESTAMP,
	"startDate"			DATE,
	"startTime"			TIME,
	"endDateTime"		TIMESTAMP,
	"endDate"			DATE,
	"endTime"			VARCHAR,
	"isDaytime"			BOOLEAN,
	"temperature"		NUMERIC,
	"temperatureUnit"	VARCHAR,
	"temperatureTrend"	VARCHAR,
	"windSpeed"			VARCHAR,
	"minWindSpeed"		NUMERIC,
	"maxWindSpeed"		NUMERIC,
	"windSpeedUnit"		VARCHAR,
	"windDirection"		VARCHAR,
	"icon"				VARCHAR,
	"shortForecast"		VARCHAR,
	"detailedForecast"	VARCHAR,
	"retrievalDateTime"	TIMESTAMP
);

SELECT * FROM "dailyForecastTB" ORDER BY "id" ASC, "retrievalDateTime" ASC;

--DELETE FROM "dailyForecastTB"

---------------------------------------------
-- Table to load Hour wise Forecast
---------------------------------------------

DROP TABLE IF EXISTS "hourlyForecastTB";

CREATE TABLE "hourlyForecastTB"
(
	"id"	SERIAL		PRIMARY KEY,
	"responseNumber"	INTEGER,
	"city"				VARCHAR,
	"latitude"			NUMERIC,
	"longitude"			NUMERIC,
	"startDateTime"		TIMESTAMP,
	"startDate"			DATE,
	"startTime"			VARCHAR,
	"endDateTime"		TIMESTAMP,
	"endDate"			DATE,
	"endTime"			VARCHAR,
	"isDaytime"			BOOLEAN,
	"temperature"		NUMERIC,
	"temperatureUnit"	VARCHAR,
	"temperatureTrend"	VARCHAR,
	"windSpeed"			VARCHAR,
	"hourWindSpeed"		NUMERIC,
	"windSpeedUnit"		VARCHAR,
	"windDirection"		VARCHAR,
	"icon"				VARCHAR,
	"shortForecast"		VARCHAR,
	"retrievalDateTime"	TIMESTAMP
);

SELECT * FROM "hourlyForecastTB";

------------------------------------------------
-- Table to store Historical Daywise Forecast
------------------------------------------------

DROP TABLE IF EXISTS "histDailyForecastTB";

CREATE TABLE "histDailyForecastTB"
(
	"histId"	SERIAL		PRIMARY KEY,
	"id"				INTEGER,
	"responseNumber"	INTEGER,
	"responseName"		VARCHAR,
	"city"				VARCHAR,
	"latitude"			NUMERIC,
	"longitude"			NUMERIC,
	"startDateTime"		TIMESTAMP,
	"startDate"			DATE,
	"startTime"			TIME,
	"endDateTime"		TIMESTAMP,
	"endDate"			DATE,
	"endTime"			VARCHAR,
	"isDaytime"			BOOLEAN,
	"temperature"		NUMERIC,
	"temperatureUnit"	VARCHAR,
	"temperatureTrend"	VARCHAR,
	"windSpeed"			VARCHAR,
	"minWindSpeed"		NUMERIC,
	"maxWindSpeed"		NUMERIC,
	"windSpeedUnit"		VARCHAR,
	"windDirection"		VARCHAR,
	"icon"				VARCHAR,
	"shortForecast"		VARCHAR,
	"detailedForecast"	VARCHAR,
	"retrievalDateTime"	TIMESTAMP
);

SELECT * FROM "dailyForecastTB";
SELECT * FROM "histDailyForecastTB";

------------------------------------------------
-- Table to store Historical Hourwise Forecast
------------------------------------------------

DROP TABLE IF EXISTS "histHourlyForecastTB";

CREATE TABLE "histHourlyForecastTB"
(
	"histId"	SERIAL		PRIMARY KEY,
	"id"				INTEGER,
	"responseNumber"	INTEGER,
	"city"				VARCHAR,
	"latitude"			NUMERIC,
	"longitude"			NUMERIC,
	"startDateTime"		TIMESTAMP,
	"startDate"			DATE,
	"startTime"			VARCHAR,
	"endDateTime"		TIMESTAMP,
	"endDate"			DATE,
	"endTime"			VARCHAR,
	"isDaytime"			BOOLEAN,
	"temperature"		NUMERIC,
	"temperatureUnit"	VARCHAR,
	"temperatureTrend"	VARCHAR,
	"windSpeed"			VARCHAR,
	"hourWindSpeed"		NUMERIC,
	"windSpeedUnit"		VARCHAR,
	"windDirection"		VARCHAR,
	"icon"				VARCHAR,
	"shortForecast"		VARCHAR,
	"retrievalDateTime"	TIMESTAMP
);

SELECT * FROM "histHourlyForecastTB";

------------------------------------------------------------------------
-- Function to be used with Trigger to load Historical Daywise Forecast
-- every time an insert is done to main Daywise Forecast table.
------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION logDailyForecastChanges()  
  RETURNS TRIGGER   
  LANGUAGE PLPGSQL  
  AS  
$$  
BEGIN  
	INSERT INTO "histDailyForecastTB"("id", "responseNumber", "responseName", "city", 	"latitude", "longitude", "startDateTime", 
									  "startDate", "startTime", "endDateTime", "endDate", "endTime", "isDaytime", "temperature", 
									  "temperatureUnit", "temperatureTrend", "windSpeed", "minWindSpeed", "maxWindSpeed", "windSpeedUnit", 
									  "windDirection", "icon", "shortForecast", "detailedForecast", "retrievalDateTime")   
	 VALUES(NEW."id", NEW."responseNumber", NEW."responseName", NEW."city", NEW."latitude", NEW."longitude", NEW."startDateTime", 
			NEW."startDate", NEW."startTime", NEW."endDateTime", NEW."endDate", NEW."endTime", NEW."isDaytime", NEW."temperature", 
			NEW."temperatureUnit", NEW."temperatureTrend", NEW."windSpeed", NEW."minWindSpeed", NEW."maxWindSpeed", NEW."windSpeedUnit", 
			 NEW."windDirection", NEW."icon", NEW."shortForecast", NEW."detailedForecast", NEW."retrievalDateTime");  

RETURN NEW;  
END;  
$$  
;


------------------------------------------------------------------------
-- Trigger to load Historical Daywise Forecast
-- every time an insert is done to main Daywise Forecast table.
------------------------------------------------------------------------
CREATE TRIGGER "loadHistDailyForecast"
AFTER INSERT 
ON "dailyForecastTB"
FOR EACH ROW
EXECUTE PROCEDURE logDailyForecastChanges();

------------------------------------------------------------------------
-- Function to be used with Trigger to load Historical Hourwise Forecast
-- every time an insert is done to main Hourwise Forecast table.
------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION logHourlyForecastChanges()  
  RETURNS TRIGGER   
  LANGUAGE PLPGSQL  
  AS  
$$  
BEGIN  
	INSERT INTO "histHourlyForecastTB"("id", "responseNumber", "city", "latitude", "longitude", "startDateTime", "startDate", "startTime",		
										"endDateTime", "endDate", "endTime", "isDaytime", "temperature", "temperatureUnit", "temperatureTrend",	
										"windSpeed", "hourWindSpeed", "windSpeedUnit", "windDirection", "icon", "shortForecast", "retrievalDateTime")  
	 VALUES(NEW."id", NEW."responseNumber", NEW."city", NEW."latitude", NEW."longitude", NEW."startDateTime", NEW."startDate", NEW."startTime",		
			NEW."endDateTime", NEW."endDate", NEW."endTime", NEW."isDaytime", NEW."temperature", NEW."temperatureUnit", NEW."temperatureTrend",	
			NEW."windSpeed", NEW."hourWindSpeed", NEW."windSpeedUnit", NEW."windDirection", NEW."icon", NEW."shortForecast", NEW."retrievalDateTime");  

RETURN NEW;  
END;  
$$  
;

------------------------------------------------------------------------
-- Trigger to load Historical Hourwise Forecast
-- every time an insert is done to main Hourwise Forecast table.
------------------------------------------------------------------------
CREATE TRIGGER "loadHistHourlyForecast"
AFTER INSERT 
ON "hourlyForecastTB"
FOR EACH ROW
EXECUTE PROCEDURE logHourlyForecastChanges();
------------------------------------------------------------------------
