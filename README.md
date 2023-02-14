# DeFi_development_process
1、Attack_events.xlsx：
This document shows all the attacks that occurred on DeFi and divides them into six categories according to the blockchain hardware hierarchy, and shows the distribution of events related to the attacks over the attack categories, as well as the discussion modes of these events.

2、Paper_list.xlsx:
This document shows a list of articles discussing attacks that occurred on blockchain, smart contracts, DeFi, and is the primary source for the list of attacks in this paper.Papers marked in blue are those discussing single attack, those marked in yellow are top journals or conferences.

3、Project_attack.xlsx:
This table shows the overall situation of project-attack related events, which is not overly represented in this paper due to the excessive content and space limitation of the article, and may be used as a direction for future research to explore the association between different types of DeFi projects and events.

4、Project_list.xlsx:
We have collected some DeFi projects with high TVL from defillama and summarized them in this table. In this paper, we need to use issues and pull requests from github as analysis data, so we must filter out projects with github links and event data, and the filtering results are shown in the table, which is available for review.

5、Supplement to Table.xlsx:
This document is a supplement to TableVII and VIII in the paper and is attached due to space limitations.The supplement to TableVII shows all the examples of attacks we collected. The supplement to TableVIII shows the average resolution time of the incidents broken down by attack types. In addition to this, there are the results of our statistics on the day of the week on which the attack occurred.

————————

6、attack_events.py:
This .py file filters out the manually matched event information related to the attack and makes it easier to calculate the average resolution time.

7、get_data.py:
This .py file is used to crawl all events data of projects.

8、raw_data.py:
This .py file is used to pre-process the crawled down metadata to retain useful information.

9、search_keywords.py:
Search for attack keywords from the title and body of events to determine that the event is related to a particular attack.

10、solved_info.py：
This .py file is used to calculate the average resolution time.

11、attack_events.zip:
Inside this zip is the basic data we have filtered for events related to the attack.
