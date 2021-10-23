---------------------------------------------
-- Table to load Daywise Forecast
---------------------------------------------
--DROP TABLE "dailyForecastTB";

CREATE TABLE "dailyForecastTB"
(
	"id"	SERIAL		PRIMARY KEY,
	"city"				VARCHAR,
	"responseNumber"	INTEGER,
	"responseName"		VARCHAR,
	"startTime"			VARCHAR,
	"endTime"			VARCHAR,
	"isDaytime"			BOOLEAN,
	"temperature"		NUMERIC,
	"temperatureUnit"	VARCHAR,
	"temperatureTrend"	VARCHAR,
	"windSpeed"			VARCHAR,
	"windDirection"		VARCHAR,
	"icon"				VARCHAR,
	"shortForecast"		VARCHAR,
	"detailedForecast"	VARCHAR,
	"runTime"			TIMESTAMP
);

SELECT * FROM "dailyForecastTB";

---------------------------------------------
-- Table to load Hour wise Forecast
---------------------------------------------

--DROP TABLE "hourlyForecastTB";

CREATE TABLE "hourlyForecastTB"
(
	"id"	SERIAL		PRIMARY KEY,
	"city"				VARCHAR,
	"responseNumber"	INTEGER,
	"responseName"		VARCHAR,
	"startTime"			VARCHAR,
	"endTime"			VARCHAR,
	"isDaytime"			BOOLEAN,
	"temperature"		NUMERIC,
	"temperatureUnit"	VARCHAR,
	"temperatureTrend"	VARCHAR,
	"windSpeed"			VARCHAR,
	"windDirection"		VARCHAR,
	"icon"				VARCHAR,
	"shortForecast"		VARCHAR,
	"detailedForecast"	VARCHAR,
	"runTime"			TIMESTAMP
);

SELECT * FROM "hourlyForecastTB";

------------------------------------------------
-- Table to store Historical Daywise Forecast
------------------------------------------------

--DROP TABLE "histDailyForecastTB";

CREATE TABLE "histDailyForecastTB"
(
	"histId"	SERIAL		PRIMARY KEY,
	"id"				INTEGER,
	"city"				VARCHAR,
	"responseNumber"	INTEGER,
	"responseName"		VARCHAR,
	"startTime"			VARCHAR,
	"endTime"			VARCHAR,
	"isDaytime"			BOOLEAN,
	"temperature"		NUMERIC,
	"temperatureUnit"	VARCHAR,
	"temperatureTrend"	VARCHAR,
	"windSpeed"			VARCHAR,
	"windDirection"		VARCHAR,
	"icon"				VARCHAR,
	"shortForecast"		VARCHAR,
	"detailedForecast"	VARCHAR,
	"runTime"			TIMESTAMP
);

SELECT * FROM "dailyForecastTB";
SELECT * FROM "histDailyForecastTB";

------------------------------------------------
-- Table to store Historical Hourwise Forecast
------------------------------------------------

--DROP TABLE "histHourlyForecastTB";

CREATE TABLE "histHourlyForecastTB"
(
	"histId"	SERIAL		PRIMARY KEY,
	"city"				VARCHAR,
	"responseNumber"	INTEGER,
	"responseName"		VARCHAR,
	"startTime"			VARCHAR,
	"endTime"			VARCHAR,
	"isDaytime"			BOOLEAN,
	"temperature"		NUMERIC,
	"temperatureUnit"	VARCHAR,
	"temperatureTrend"	VARCHAR,
	"windSpeed"			VARCHAR,
	"windDirection"		VARCHAR,
	"icon"				VARCHAR,
	"shortForecast"		VARCHAR,
	"detailedForecast"	VARCHAR,
	"runTime"			TIMESTAMP
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
	INSERT INTO "histDailyForecastTB"("id", "city", "responseNumber", "responseName", "startTime", "endTime", 
									  "isDaytime", "temperature", "temperatureUnit", "temperatureTrend", "windSpeed", 
									  "windDirection", "icon", "shortForecast", "detailedForecast", "runTime")  
	 VALUES(NEW."id" , NEW."city", NEW."responseNumber", NEW."responseName", NEW."startTime", NEW."endTime", 
			NEW."isDaytime", NEW."temperature", NEW."temperatureUnit", NEW."temperatureTrend", NEW."windSpeed", 
			NEW."windDirection", NEW."icon", NEW."shortForecast", NEW."detailedForecast", NEW."runTime");  
RETURN NEW;  
END;  
$$  

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
	INSERT INTO "histHourlyForecastTB"("id", "city", "responseNumber", "responseName", "startTime", "endTime", 
									   "isDaytime", "temperature", "temperatureUnit", "temperatureTrend", "windSpeed", 
									   "windDirection", "icon", "shortForecast", "detailedForecast", "runTime")  
	 VALUES(NEW."id" , NEW."city", NEW."responseNumber", NEW."responseName", NEW."startTime", NEW."endTime", 
			NEW."isDaytime", NEW."temperature", NEW."temperatureUnit", NEW."temperatureTrend", NEW."windSpeed", 
			NEW."windDirection", NEW."icon", NEW."shortForecast", NEW."detailedForecast", NEW."runTime");  
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
