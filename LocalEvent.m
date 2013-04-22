//
//  LocalEvent.m
//  LocalMusic
//
//  Created by Elizabeth Chaddock on 4/8/13.
//  Copyright (c) 2013 Elizabeth Chaddock. All rights reserved.
//

#import "LocalEvent.h"

@implementation LocalEvent
-(id)initWithName:(NSString *)name location:(NSString *)location date:(NSDate *)date {
    self = [super init];
    if(self) {
        _bandName = name;
        _location = location;
        _date = date;
        return self;
    }
    return nil;
}
@end
