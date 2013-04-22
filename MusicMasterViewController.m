//
//  MusicMasterViewController.m
//  LocalMusic
//
//  Created by Elizabeth Chaddock on 4/3/13.
//  Copyright (c) 2013 Elizabeth Chaddock. All rights reserved.
//
#define kBgQueue dispatch_get_global_queue( DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)
#define eventsPulled [NSURL URLWithString: @"http://api.seatgeek.com/2/events?geoip=true"]

#import "MusicMasterViewController.h"

#import "MusicDataController.h"
#import "LocalEvent.h"
#import "MusicDetailViewController.h"

@implementation MusicMasterViewController

- (void)awakeFromNib
{
    [super awakeFromNib];
    self.dataController = [[MusicDataController alloc] init];
}

- (void)viewDidLoad
{
    
    [super viewDidLoad];
    
    self.navigationItem.rightBarButtonItem.accessibilityHint = @"Adds a new event";
    
	// Do any additional setup after loading the view, typically from a nib.
    
    /*dispatch_async(kBgQueue, ^{
        NSData* data = [NSData dataWithContentsOfURL: eventsPulled];
        
        [self performSelectorOnMainThread:@selector(fetchedData:)
                               withObject:data waitUntilDone:YES];
    });*/
    
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Table View

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView
{
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return [self.dataController countOfList];
}

/*
 * Get an event at an index
 */
- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    static NSString *CellIdentifier = @"LocalEventCell";
    
    static NSDateFormatter *formatter = nil;
    
    if (formatter == nil) {
        formatter = [[NSDateFormatter alloc] init];
        [formatter setDateStyle:NSDateFormatterMediumStyle];
    }
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier];
    
    LocalEvent *eventAtIndex = [self.dataController objectInListAtIndex:indexPath.row];
    
    [[cell textLabel] setText:eventAtIndex.bandName];
    [[cell detailTextLabel] setText:[formatter stringFromDate:(NSDate *)eventAtIndex.date]];
    return cell;
}

- (BOOL)tableView:(UITableView *)tableView canEditRowAtIndexPath:(NSIndexPath *)indexPath {
    return NO;
}

- (void)fetchedData:(NSData *)responseData {
    NSError* error;
    NSDictionary* json = [NSJSONSerialization JSONObjectWithData:responseData
                                                         options:kNilOptions
                                                           error:&error];
    NSArray* latestEvents = [json objectForKey:@"events"];
    //NSLog(@"bands: %@", latestEvents);
    
    NSDictionary* event = [latestEvents objectAtIndex:1];
    NSDictionary* performer = [(NSArray*)[event objectForKey:@"performers"] objectAtIndex:0];
    if([[performer objectForKey:@"type"] isEqualToString:@"band"])
    {
        //set the artist's name
        NSString* name = [performer objectForKey:@"name"];
        NSLog(@"performer: %@", name);
        
        //set the venue
        //NSDictionary* venue = [(NSArray*)[event objectForKey:@"venue"] objectAtIndex:0];
        //NSString *venueName = [venue objectForKey:@"name"];
        NSString *venueName = @"Liz's party mansion";
        
        //Set the date
        //NSString* d = [event objectForKey:@"datetime_local"];
        //NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
        //[dateFormatter setDateFormat:@"yyyy-MM-DDTHH:mm:ss"];
        //NSDate* date = [dateFormatter dateFromString:d];
        NSDate* date = [NSDate date];
        
        LocalEvent* newEvent;
        newEvent = [[LocalEvent alloc] initWithName:name location:venueName date:date];
        [self.dataController addLocalEventWithEvent:newEvent];
    }
}

- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    if ([[segue identifier] isEqualToString:@"ShowEventDetails"]) {
        MusicDetailViewController *detailViewController = [segue destinationViewController];
        
        detailViewController.event = [self.dataController objectInListAtIndex:[self.tableView indexPathForSelectedRow].row];
    }
}


@end
