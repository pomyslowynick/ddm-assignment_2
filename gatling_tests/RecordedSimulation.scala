package hars.k8s_test

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.jdbc.Predef._

class RecordedSimulation extends Simulation {

	val httpProtocol = http
		.baseUrl("http://127.0.0.1:30001")
		.inferHtmlResources()
		.acceptHeader("application/json, text/javascript, */*; q=0.01")
		.acceptEncodingHeader("gzip, deflate")
		.acceptLanguageHeader("en-US,en;q=0.5")
		.doNotTrackHeader("1")
		.userAgentHeader("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0")

	val headers_0 = Map(
		"Accept" -> "*/*",
		"Accept-Encoding" -> "gzip, deflate, br")

	val headers_1 = Map(
		"Accept" -> "text/css,*/*;q=0.1",
		"Accept-Encoding" -> "gzip, deflate, br",
		"Origin" -> "http://127.0.0.1:30001")

	val headers_2 = Map(
		"Accept" -> "*/*",
		"Accept-Encoding" -> "gzip, deflate, br",
		"Origin" -> "http://127.0.0.1:30001")

	val headers_5 = Map("X-Requested-With" -> "XMLHttpRequest")
	
	def getAnalyticsData() = {
		repeat(5) {      exec(http("request_12")
			.get("/get_data")
			.headers(headers_5)
			.resources(http("request_13")
			.get("/get_data")
			.headers(headers_5)
			.check(status.in(200)))
			.check(status.in(200)))
    	}
  	}
	val scn = scenario("RecordedSimulation")
		.exec(getAnalyticsData())
		.pause(5)
		.exec(getAnalyticsData())
		.pause(10)
		.exec(getAnalyticsData())

	setUp(scn.inject(atOnceUsers(3))).protocols(httpProtocol)
}