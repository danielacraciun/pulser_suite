package com.example.dana.environmentdataminer.models;

import android.provider.BaseColumns;

/**
 * Created by dana on 5/23/17.
 */

public class MinerKey {
    // To prevent someone from accidentally instantiating the contract class,
    // make the constructor private.
    private MinerKey() {}

    /* Inner class that defines the table contents */
    public static class keyEntry implements BaseColumns {
        public static final String TABLE_NAME = "skey";
        public static final String COLUMN_NAME_VAL= "value";
    }

     static final String SQL_CREATE_ENTRIES =
            "CREATE TABLE " + keyEntry.TABLE_NAME + " (" +
                    keyEntry._ID + " INTEGER PRIMARY KEY," +
                    keyEntry.COLUMN_NAME_VAL + " TEXT)";

     static final String SQL_DELETE_ENTRIES =
            "DROP TABLE IF EXISTS " + keyEntry.TABLE_NAME;
}
