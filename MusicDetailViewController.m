//
//  MusicDetailViewController.m
//  LocalMusic
//
//  Created by Elizabeth Chaddock on 4/8/13.
//  Copyright (c) 2013 Elizabeth Chaddock. All rights reserved.
//

#import "MusicDetailViewController.h"
#import "LocalEvent.h"
@interface MusicDetailViewController ()
- (void)configureView;
@end

@implementation MusicDetailViewController

#pragma mark - Managing the detail item

- (void)setEvent:(LocalEvent *) newEvent
{
    if(_event != newEvent) {
        _event = newEvent;
        
        //Update the view
        [self configureView];
    }
}

- (void)configureView
{
    // Update the user interface for the detail item.
    LocalEvent *theEvent = self.event;
    
    static NSDateFormatter *formatter = nil;
    if (formatter == nil) {
        formatter = [[NSDateFormatter alloc] init];
        [formatter setDateStyle:NSDateFormatterMediumStyle];
    }
    if (theEvent) {
        self.bandNameLabel.text = theEvent.bandName;
        self.locationLabel.text = theEvent.location;
        self.dateLabel.text = [formatter stringFromDate:(NSDate *)theEvent.date];
    }
    
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    [self configureView];
}


@end
