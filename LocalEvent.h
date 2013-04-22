//
//  LocalEvent.h
//  LocalMusic
//
//  Created by Elizabeth Chaddock on 4/8/13.
//  Copyright (c) 2013 Elizabeth Chaddock. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface LocalEvent : NSObject
@property (nonatomic, copy) NSString *bandName;
@property (nonatomic, copy) NSString *location;
@property (nonatomic, strong) NSDate *date;
-(id)initWithName:(NSString *)name location:(NSString *)location date:(NSDate *)date;
@end
