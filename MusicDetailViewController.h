//
//  EventsDetailViewController.h
//  LocalMusic
//
//  Created by Elizabeth Chaddock on 4/8/13.
//  Copyright (c) 2013 Elizabeth Chaddock. All rights reserved.
//

#import <UIKit/UIKit.h>
@class LocalEvent;

@interface MusicDetailViewController : UITableViewController
@property (strong, nonatomic) LocalEvent *event;
@property (weak, nonatomic) IBOutlet UILabel *bandNameLabel;
@property (weak, nonatomic) IBOutlet UILabel *locationLabel;
@property (weak, nonatomic) IBOutlet UILabel *dateLabel;
@end
