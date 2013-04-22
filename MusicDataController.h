//
//  LocalMusicDataController.h
//  LocalMusic
//
//  Created by Elizabeth Chaddock on 4/8/13.
//  Copyright (c) 2013 Elizabeth Chaddock. All rights reserved.
//

#import <Foundation/Foundation.h>

@class LocalEvent;

@interface MusicDataController : NSObject
@property (nonatomic, copy) NSMutableArray *masterEventList;
- (NSUInteger)countOfList;
- (LocalEvent *) objectInListAtIndex:(NSUInteger)theIndex;
- (void)addLocalEventWithEvent:(LocalEvent *)event;
@end
