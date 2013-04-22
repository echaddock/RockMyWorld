//
//  MusicMasterViewController.h
//  LocalMusic
//
//  Created by Elizabeth Chaddock on 4/3/13.
//  Copyright (c) 2013 Elizabeth Chaddock. All rights reserved.
//

#import <UIKit/UIKit.h>
@class MusicDataController;

@interface MusicMasterViewController:UITableViewController
//IBOutlet UILabel* humanReadable;
@property (strong, nonatomic) MusicDataController *dataController;
//- (IBAction)done:(UIStoryboardSegue *)segue;
//- (IBAction)cancel:(UIStoryboardSegue *)segue;
@end