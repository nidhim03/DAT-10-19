"""
Homework 1 
Oore Ladipo
11/06/2020
"""
import requests
from requests_oauthlib import OAuth1

auth = OAuth1('r8ZOzLMZoouq5u8iCdmNKiSMx', 'tIqgdrMHBrkMRXfBlY36cUpxDw34LygVL9hBg5A4Dl0yIQLOAb','1216043853284827136-XgLCLf15GtZZ0oIsgInUIjJT1lnPmT', 'ksKmplYg3WBqwThvTbhknJmhBYE7t43Bt0ZijmExr2Nq2')


#Function 1
def find_user(name,keys = ['id', 'id_str', 'name', 'screen_name', 'location', 'description', 'url',
     'entities', 'protected', 'followers_count', 'friends_count',
     'listed_count', 'created_at', 'favourites_count', 'utc_offset',
     'time_zone', 'geo_enabled', 'verified', 'statuses_count', 'lang',
     'status', 'contributors_enabled', 'is_translator',
     'is_translation_enabled', 'profile_background_color',
     'profile_background_image_url', 'profile_background_image_url_https',
     'profile_background_tile', 'profile_image_url',
     'profile_image_url_https', 'profile_banner_url', 'profile_link_color',
     'profile_sidebar_border_color', 'profile_sidebar_fill_color',
     'profile_text_color', 'profile_use_background_image',
     'has_extended_profile', 'default_profile', 'default_profile_image',
     'following', 'follow_request_sent', 'notifications', 'translator_type']):
  """
  This function finds if a user object exists for the twitter handle returned
  as a required input it accepts the user_name - a user's twitter handle
  as optional inputs it accepts user parameters by which to filter the output. These parameters are entered as a list of strings
  as output it returns a dictionary that represents the users's twitter information
  """
    
  #This line checks to see if the string begins with an @ and removes it
  name = name.strip("@").lower()
    
  #this returns the user details if the user exists or returns an empty dictionary if the user does not exist
  try:
      api_url ='https://api.twitter.com/1.1/users/lookup.json?screen_name={}'.format(name)
      user_details = requests.get(api_url, auth=auth)
      output = { key: user_details.json()[0][key] for key in keys }
      return output
  except:
    print("No user exists with the handle {}".format(name))
    return {}


#Function 2
def find_hashtag(hashtag, count = 20, search_type = 'mixed'):
    """
    This function finds related tweets that are tagged with a specific hashtag
    as a required input it accepts the hashtag with or without the #
    as one of the optional inputs it accepts the count of tweets required to be returned 
    as another optional input it accepts the search type as either recent, mixed, or popular
    as output it returns a list of data objects containing information about the tweets returned
    """
    
    #This line checks to see if the string begins with a # and removes it
    half_hash = hashtag.strip("#").lower()
    hashtag = '%23'+hashtag.strip("#").lower()
    
    #this returns the user details if the user exists or returns an empty dictionary if the user does not exist
    try:
        api_url ='https://api.twitter.com/1.1/search/tweets.json?q={}&count={}&result_type={}'.format(hashtag,count,search_type)
        selected_tweets = requests.get(api_url, auth=auth)
        # i'm not sure what a list of data objects here refers to and so I'm choosing to return what I think is most appropriate
        return selected_tweets.json()['statuses']
        #alternative solutions include the two options below
        #return selected_tweets.json()['search_metadata']
        #return [selected_tweets.json()]
        
    except:
        print("There was an error associated with your input")
        return []


#Function 3
def get_followers(name, keys = ['name', 'followers_count', 'friends_count', 'screen_name'], to_df=False):
    """
    This function finds if a user exists for the twitter handle and details about the users' followers
    as a required input it accepts the user_name - a user's twitter handle
    as optional inputs it accepts parameters by which to filter the output. These parameters are entered as a list of strings
    as output it returns either a list of data objects on each of the users followers or a dataFrame of the same information
    """
    
    #This line checks to see if the string begins with an @ and removes it
    name = name.strip("@").lower()
    
    #this returns the user details if the user exists or returns an empty dictionary if the user does not exist
    user_data = []
    
    api_url ='https://api.twitter.com/1.1/followers/list.json?screen_name={}'.format(name)
    user_details = requests.get(api_url, auth=auth)
    users_list = user_details.json()['users']

    
    try:
        api_url ='https://api.twitter.com/1.1/followers/list.json?screen_name={}'.format(name)
        user_details = requests.get(api_url, auth=auth)
        users_list = user_details.json()['users']
        
        for user in users_list:
            output = {}
            for key in keys:
                output[key]=user[key]
            user_data.append(output)
        
        if to_df == True:
            return pd.DataFrame(user_data)
        else:
            return user_data
    except:
        print("There was an error associated with your input")
        
        if to_df == True:
            return pd.DataFrame(user_data)
        else:
            return user_data



#Function 4
def friends_of_friends(people, keys = ['id', 'id_str', 'name', 'screen_name', 'location'
    , 'description', 'url', 'entities', 'protected', 'followers_count', 'friends_count', 'listed_count'
    , 'created_at', 'favourites_count', 'utc_offset', 'time_zone', 'geo_enabled', 'verified', 'statuses_count'
    , 'lang', 'status', 'contributors_enabled', 'is_translator', 'is_translation_enabled', 'profile_background_color'
    , 'profile_background_image_url', 'profile_background_image_url_https', 'profile_background_tile'
    , 'profile_image_url', 'profile_image_url_https', 'profile_banner_url', 'profile_link_color'
    , 'profile_sidebar_border_color', 'profile_sidebar_fill_color', 'profile_text_color'
    , 'profile_use_background_image', 'has_extended_profile', 'default_profile', 'default_profile_image'
    , 'following', 'live_following', 'follow_request_sent', 'notifications', 'muting', 'blocking'
    , 'blocked_by', 'translator_type']
    , to_df=False):

    """
    This function finds if friends are shared between two users
    as a required input it accepts a list of usernames 
    as optional inputs it accepts keys by which to filter the output. These parameters are entered as a list of strings
    as optional input it accepts a flag that helps decide if the returned value should be a DataFrame or a list
    as output it returns either a list of data objects on each of the users followers or a dataFrame of the same information
    """

    #This line checks to see if the names begins with an @ and removes it
    people = [name.strip("@").lower() for name in people]

    #useful lists for later
    all_user_ids = []
    all_user_data = []
    output = []

    
    #getting the list of friends for each name in the people list
    for name in people:
        api_url ='https://api.twitter.com/1.1/friends/list.json?screen_name={}'.format(name)
        user_details = requests.get(api_url, auth=auth)
        friends_list = user_details.json()['users']
        friend_ids = []
        #for each name we add the user_id into the all_user_ids list and the data into the all_user_data list
        for people in friends_list:
            friend_ids.append(people['id'])
            all_user_data.append(people)
        all_user_ids.append(friend_ids)
    
    #this helps us figure out the shared friends between the people
    shared_friends = [x for x in all_user_ids[0] if x in all_user_ids[1]]
    
    #doing this to eliminate duplicate records
    deduped_user_list = [] 
    for i in range(len(all_user_data)): 
        if all_user_data[i] not in all_user_data[i + 1:]: 
            deduped_user_list.append(all_user_data[i]) 
    all_user_data = deduped_user_list

    #this is where we select our output based on the shared friends
    for user_data in all_user_data:
        if user_data['id'] in shared_friends:
            output.append(user_data)

    if to_df == False:
        return output
    else:
        return pd.DataFrame(output)


#Function 5
def friends_of_friends(people, keys = ['id', 'id_str', 'name', 'screen_name', 'location'
    , 'description', 'url', 'entities', 'protected', 'followers_count', 'friends_count', 'listed_count'
    , 'created_at', 'favourites_count', 'utc_offset', 'time_zone', 'geo_enabled', 'verified', 'statuses_count'
    , 'lang', 'status', 'contributors_enabled', 'is_translator', 'is_translation_enabled', 'profile_background_color'
    , 'profile_background_image_url', 'profile_background_image_url_https', 'profile_background_tile'
    , 'profile_image_url', 'profile_image_url_https', 'profile_banner_url', 'profile_link_color'
    , 'profile_sidebar_border_color', 'profile_sidebar_fill_color', 'profile_text_color'
    , 'profile_use_background_image', 'has_extended_profile', 'default_profile', 'default_profile_image'
    , 'following', 'live_following', 'follow_request_sent', 'notifications', 'muting', 'blocking'
    , 'blocked_by', 'translator_type']
    , to_df=False
    , full_search = False):

    """
    This function finds if friends are shared between two users
    as a required input it accepts a list of usernames 
    as optional inputs it accepts keys by which to filter the output. These parameters are entered as a list of strings
    as optional input it accepts a flag that helps decide if the returned value should be a DataFrame or a list
    as output it returns either a list of data objects on each of the users followers or a dataFrame of the same information
    """

    #This line checks to see if the names begins with an @ and removes it
    people = [name.strip("@").lower() for name in people]

    #useful lists for later
    all_user_ids = []
    all_user_data = []
    output = []

    if full_search == False:
        #getting the list of friends for each name in the people list
        for name in people:
            api_url ='https://api.twitter.com/1.1/friends/list.json?screen_name={}'.format(name)
            user_details = requests.get(api_url, auth=auth)
            friends_list = user_details.json()['users']
            friend_ids = []
            #for each name we add the user_id into the all_user_ids list and the data into the all_user_data list
            for people in friends_list:
                friend_ids.append(people['id'])
                all_user_data.append(people)
            all_user_ids.append(friend_ids)
    else:
        cursor = -1
        #getting the complete list of friends for each name in the people list
        for name in people:
            while cursor != 0:
                api_url ='https://api.twitter.com/1.1/friends/list.json?screen_name={}'.format(name)
                user_details = requests.get(api_url, auth=auth)
                friends_list = user_details.json()['users']
                cursor = user_details.json()['next_cursor']
                friend_ids = []
                #for each name we add the user_id into the all_user_ids list and the data into the all_user_data list
                for people in friends_list:
                    friend_ids.append(people['id'])
                    all_user_data.append(people)
            all_user_ids.append(friend_ids)
    
    #this helps us figure out the shared friends between the people
    shared_friends = [x for x in all_user_ids[0] if x in all_user_ids[1]]
    
    #doing this to eliminate duplicate records
    deduped_user_list = [] 
    for i in range(len(all_user_data)): 
        if all_user_data[i] not in all_user_data[i + 1:]: 
            deduped_user_list.append(all_user_data[i]) 
    all_user_data = deduped_user_list

    #this is where we select our output based on the shared friends
    for user_data in all_user_data:
        if user_data['id'] in shared_friends:
            output.append(user_data)

    if to_df == False:
        return output
    else:
        return pd.DataFrame(output)


