def gsuite_group(email):
    import pickle
    import os.path
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/admin.directory.group.readonly',
              'https://www.googleapis.com/auth/admin.directory.user.readonly',
              ]
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    service = build('admin', 'directory_v1', credentials=creds)
    results = service.groups().list(customer='my_customer', query=f"memberKey={email}").execute()
    gsuite_gr = results.get('groups')
    # print(gsuite_gr)
    for item in gsuite_gr:
        # keys = item.keys() "Show you all the keys you can filter from"
        # print(keys)  "Show you all the keys you can filter from"
        emails = item.get('email')
        name = item.get('name')
        aliases = item.get('aliases')
        directmembers = item.get('directMembersCount')
        print(f"Group: {name} ({emails}) \n Aliases: "
              f"{aliases} \n Members: {directmembers} \n")


gsuite_group('Enter Email Address')
