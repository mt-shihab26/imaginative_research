export const INTEGER = "INTEGER";
export const PLUS = "PLUS";
export const MINUS = "MINUS";
export const ASTERISK = "ASTERISK";
export const SLASH = "SLASH";

export type TTokenType = string;

export type TToken = {
    type: TTokenType;
    literal: string;
};
