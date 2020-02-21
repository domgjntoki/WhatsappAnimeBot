def get_anilist_api_url():
    return 'https://graphql.anilist.co'


def get_release_from_anime_q():
    q = '''
        query ($id: Int, $idMal_in: [Int], $search: String, 
                $page: Int, $perPage: Int, $format_in: [MediaFormat], 
                $startDate_greater:  FuzzyDateInt) {
            Page (page: $page, perPage: $perPage) {
                pageInfo {
                    total
                    currentPage
                    lastPage
                    hasNextPage
                    perPage
                }
                media (id: $id, idMal_in: $idMal_in, search: $search, 
                        startDate_greater: $startDate_greater, 
                        type: ANIME, format_in: $format_in,
                        status_in: [NOT_YET_RELEASED, RELEASING], 
                        sort: START_DATE_DESC) {
                    id
                    coverImage {
                        large
                        medium
                    }
                    
                    idMal
                    type
                    format
                    season
                    status
                    episodes
                    title {
                        romaji
                        english
                        native
                    }
                    synonyms
                    startDate {
                        day
                        year
                        month
                    }
                    endDate {
                        day,
                        year,
                        month
                    }
                    nextAiringEpisode { 
                        airingAt
                        timeUntilAiring
                        episode
                    }
                }
            }
        }
        '''
    return q


def get_studio_search_q():
    q = '''
    query ($id: Int, $search: String, $page: Int, $perPage: Int) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            studios(id: $id, search: $search) {
                id
                name
                media(sort: POPULARITY_DESC, isMain: true, 
                      page: 1, perPage: 50) {
                    nodes {
                        id
                        idMal
                        title {
                            romaji
                            english
                            native
                        }
                        synonyms

                        coverImage {
                            large
                            medium
                        }
                        type
                        format
                        season
                        status
                        episodes
                        startDate {
                            day
                            year
                            month
                        }
                        endDate {
                            day,
                            year,
                            month
                        }
                    }
                }
            }
        }
    }
    '''
    return q