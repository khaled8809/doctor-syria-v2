declare module 'quagga' {
  interface QuaggaConfig {
    inputStream?: {
      name?: string;
      type?: string;
      target?: any;
      constraints?: {
        width?: number;
        height?: number;
        facingMode?: string;
      };
      area?: {
        top?: string;
        right?: string;
        left?: string;
        bottom?: string;
      };
    };
    decoder?: {
      readers?: string[];
    };
    locate?: boolean;
  }

  interface QuaggaResult {
    codeResult: {
      code: string;
      format: string;
    };
  }

  export function init(config: QuaggaConfig, callback?: (err: any) => void): void;
  export function start(): void;
  export function stop(): void;
  export function onDetected(callback: (result: QuaggaResult) => void): void;
  export function offDetected(callback: (result: QuaggaResult) => void): void;
}
