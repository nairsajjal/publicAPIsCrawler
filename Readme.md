# Postman Assignment - Public APIs Crawler

* This project crawls the entire list of APIs present in this api- https://documenter.getpostman.com/view/4796420/SzmZczsh?version=latest#747c429e-709b-44e2-b4a7-89b5e6582fff and then stores the entire result in a database(MongoDB).  

## Important point about the project

1. To retrieve the list of categories from the API, a token is required from the server for authentication and that token will remain valid for 5 mins, this is being done by the fetchToken() method of the Fetcher Class.

2. Every API has a limited request rate, and this API has a rate of 10 per minute, in oder to manage the rate limit this project throttles the amount of requests by adding sleep and making sure that only 10 requests/minute are made.

3. To regulate the rate limit, the semaphore is used to throttle the current request by adding sleep and making sure that only allowed number of requests are made per minute.

4. The crawled data is then written in a JSON file which is then stored in a MongoDB database, this project uses mlab to store the MongoDB database schema.

## Steps to run the project
### Requirements - Git, Docker on the local system
1. Run command `git clone https://github.com/nairsajjal/publicAPIsCrawlertest.git`
2. Execute `sudo dockerd`
3. Execute `docker-compose up`.

## Details of all the tables and their schema

Database used - PostgreSQL

Schema- 
| Column      | Description |
| ---         | ---         |
| API         | TEXT        |
| Description | TEXT        |
| Auth        | TEXT        |
| HTTPS       | BOOLEAN     |
| Cors        | TEXT        |
| Link        | TEXT        |
| Category    | TEXT        |

Code to recreate the tables:
    CREATE TABLE sudhan_postmanapi (
	"API" TEXT, 
	"Description" TEXT, 
	"Auth" TEXT, 
	"HTTPS" BOOLEAN, 
	"Cors" TEXT, 
	"Link" TEXT, 
	"Category" TEXT
    )


## Points to achieve (That I have achieved)

1. Your code should follow concept of OOPS
2. Support for handling authentication requirements & token expiration of server
3. Support for pagination to get all data
4. Develop work around for rate limited server
5. Crawled all API entries for all categories and stored it in a database

## Things that could have been improved(if I had more days)

-  A frontend View in ReactJS to visualize the database, and then deploy this entire project on Heroku, this would provide a better user experience and the steps required to run this project will be reduced to only one step that is calling the address in a browser.

-  Add checkpoints in dockerfile to save the state of the container and reload from the last checkpoint if any error occurs.
