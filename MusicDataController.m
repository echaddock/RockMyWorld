//
//  MusicDataController.m
//  LocalMusic
//
//  Created by Elizabeth Chaddock on 4/8/13.
//  Copyright (c) 2013 Elizabeth Chaddock. All rights reserved.
//
#define kBgQueue dispatch_get_global_queue( DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)
#define eventsPulled [NSURL URLWithString: @"http://api.seatgeek.com/2/events?geoip=true&per_page=30"]


#import "MusicDataController.h"
#import "LocalEvent.h"

@interface MusicDataController ()
- (void) initializeDefaultDataList;
@end

@implementation MusicDataController

/*
 * Initialize backing mutable array of events
 */
- (void) initializeDefaultDataList {
    NSMutableArray *eventList = [[NSMutableArray alloc] init];
    self.masterEventList = eventList;
    //LocalEvent *event;
   // NSDate *date = [NSDate date]; //getting today's date
    //event = [[LocalEvent alloc] initWithName:@"Jonas Brothers" location:@"Porter's Pub" date:date];
    //[self addLocalEventWithEvent:event];
        NSData* data = [NSData dataWithContentsOfURL: eventsPulled];
         [self fetchedData:data];
}

- (void)fetchedData:(NSData *)responseData {

NSError* error;
NSDictionary* json = [NSJSONSerialization JSONObjectWithData:responseData
                                                     options:kNilOptions
                                                       error:&error];
NSArray* latestEvents = [json objectForKey:@"events"];
//NSLog(@"bands: %@", latestEvents);

    for(NSDictionary* event in latestEvents)
    {
        //NSDictionary* event = [latestEvents objectAtIndex:1];
        NSDictionary* performer = [(NSArray*)[event objectForKey:@"performers"] objectAtIndex:0];
        if([[performer objectForKey:@"type"] isEqualToString:@"band"])
        {
            //set the artist's name
            NSString* name = [performer objectForKey:@"name"];
            NSLog(@"performer: %@", name);
    
            //set the venue
            NSDictionary* venue = (NSDictionary*)[event objectForKey:@"venue"];
            NSString* venueName = [venue objectForKey:@"name"];
            
            //Set the date
            NSString* d = [event objectForKey:@"datetime_local"];
            NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
            [dateFormatter setDateFormat:@"yyyy-MM-dd'T'HH:mm:ss"];
            NSDate* date = [dateFormatter dateFromString:d];
            LocalEvent* newEvent;
            newEvent = [[LocalEvent alloc] initWithName:name location:venueName date:date];
            [self addLocalEventWithEvent:newEvent];
            //add event, score kv pair to NSDictionary
         }
    }
    
    //Add events to UI based on ordering returned by sorting by score
}

/*
 * Reset the list
 */
- (void) setMasterEventList:(NSMutableArray *)newList
{
    if(_masterEventList != newList) {
        _masterEventList = [newList mutableCopy];
    }
}

-(id)init {
    if (self = [super init]) {
        [self initializeDefaultDataList];
        return self;
    }
    return nil;
}

/*
 * Get the number of events in the array
 */
- (NSUInteger)countOfList {
    return [self.masterEventList count];
}

- (LocalEvent *)objectInListAtIndex:(NSUInteger)theIndex {
    return [self.masterEventList objectAtIndex:theIndex];
}

/*
 * Add a local event to the array
 */
- (void)addLocalEventWithEvent:(LocalEvent *)event {
    [self.masterEventList addObject:event];
}

@end