# Frontend Build Process Streamlining Implementation Plan

## Overview

This document provides a comprehensive implementation plan for streamlining the frontend build process in the PiWardrive project. The goal is to optimize developer experience, improve build performance, enable hot module replacement, and create an efficient development workflow.

## Current State Analysis

### Existing Build Process

- Basic React application with Create React App
- Standard webpack configuration
- No hot module replacement
- Limited build optimization
- No bundle analysis tools
- Manual deployment process

### Performance Issues

- Long build times during development
- Full page reloads on code changes
- Large bundle sizes
- No code splitting
- No tree shaking optimization
- No caching strategies

## Implementation Strategy

### Phase 1: Modern Build Tool Migration (Week 1-2)

#### 1.1 Vite Migration Setup

**File: `webui/vite.config.js`**

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react({
      // Enable Fast Refresh for better development experience
      fastRefresh: true,
      // Enable JSX runtime
      jsxRuntime: 'automatic'
    }),
    // Bundle analyzer
    visualizer({
      filename: 'dist/stats.html',
      open: true,
      gzipSize: true,
      brotliSize: true
    })
  ],
  
  // Development server configuration
  server: {
    port: 3000,
    host: true,
    hmr: {
      overlay: true
    },
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  
  // Build configuration
  build: {
    outDir: 'dist',
    sourcemap: true,
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    },
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  },
  
  // Path resolution
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@components': resolve(__dirname, 'src/components'),
      '@pages': resolve(__dirname, 'src/pages'),
      '@utils': resolve(__dirname, 'src/utils'),
      '@services': resolve(__dirname, 'src/services'),
      '@hooks': resolve(__dirname, 'src/hooks'),
      '@assets': resolve(__dirname, 'src/assets')
    }
  },
  
  // CSS configuration
  css: {
    modules: {
      localsConvention: 'camelCaseOnly'
    },
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    }
  },
  
  // Optimization
  optimizeDeps: {
    include: ['react', 'react-dom', 'react-router-dom'],
    exclude: ['@vite/client', '@vite/env']
  },
  
  // Environment variables
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    __BUILD_DATE__: JSON.stringify(new Date().toISOString())
  }
});
```

#### 1.2 Package.json Updates

**File: `webui/package.json`**

```json
{
  "name": "piwardrive-webui",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "analyze": "vite build --mode analyze",
    "lint": "eslint src --ext js,jsx,ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint src --ext js,jsx,ts,tsx --fix",
    "format": "prettier --write src/**/*.{js,jsx,ts,tsx,json,css,scss,md}",
    "format:check": "prettier --check src/**/*.{js,jsx,ts,tsx,json,css,scss,md}",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage",
    "type-check": "tsc --noEmit",
    "clean": "rm -rf dist node_modules/.vite",
    "prebuild": "npm run clean && npm run lint && npm run type-check",
    "postbuild": "npm run analyze"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.15.0",
    "lucide-react": "^0.263.1",
    "clsx": "^2.0.0",
    "tailwind-merge": "^1.14.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "@vitejs/plugin-react": "^4.0.3",
    "@vitest/ui": "^0.34.1",
    "autoprefixer": "^10.4.14",
    "eslint": "^8.45.0",
    "eslint-plugin-react": "^7.32.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.3",
    "jsdom": "^22.1.0",
    "postcss": "^8.4.27",
    "prettier": "^3.0.0",
    "rollup-plugin-visualizer": "^5.9.2",
    "tailwindcss": "^3.3.0",
    "typescript": "^5.0.2",
    "vite": "^4.4.5",
    "vitest": "^0.34.1"
  }
}
```

#### 1.3 TypeScript Configuration

**File: `webui/tsconfig.json`**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@pages/*": ["src/pages/*"],
      "@utils/*": ["src/utils/*"],
      "@services/*": ["src/services/*"],
      "@hooks/*": ["src/hooks/*"],
      "@assets/*": ["src/assets/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### Phase 2: Development Experience Enhancements (Week 2-3)

#### 2.1 Hot Module Replacement Setup

**File: `webui/src/main.jsx`**

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Hot Module Replacement
if (import.meta.hot) {
  import.meta.hot.accept('./App', () => {
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
  });
}
```

#### 2.2 Development Tools Configuration

**File: `webui/.eslintrc.js`**

```javascript
module.exports = {
  root: true,
  env: {
    browser: true,
    es2020: true,
    node: true
  },
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:react/jsx-runtime'
  ],
  ignorePatterns: ['dist', '.eslintrc.js'],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true
    }
  },
  settings: {
    react: {
      version: 'detect'
    }
  },
  plugins: [
    'react',
    'react-hooks',
    'react-refresh',
    '@typescript-eslint'
  ],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true }
    ],
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
    'react/prop-types': 'off',
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/no-explicit-any': 'warn',
    'no-console': 'warn',
    'no-debugger': 'error',
    'prefer-const': 'error',
    'no-var': 'error'
  }
};
```

#### 2.3 Prettier Configuration

**File: `webui/.prettierrc.js`**

```javascript
module.exports = {
  semi: true,
  trailingComma: 'es5',
  singleQuote: true,
  printWidth: 80,
  tabWidth: 2,
  useTabs: false,
  bracketSpacing: true,
  bracketSameLine: false,
  arrowParens: 'avoid',
  endOfLine: 'lf',
  quoteProps: 'as-needed',
  jsxSingleQuote: true,
  overrides: [
    {
      files: '*.json',
      options: {
        printWidth: 200
      }
    }
  ]
};
```

### Phase 3: Build Optimization (Week 3-4)

#### 3.1 Code Splitting Implementation

**File: `webui/src/components/LazyComponent.jsx`**

```javascript
import { lazy, Suspense } from 'react';
import { Loader2 } from 'lucide-react';

const createLazyComponent = (importFunc, fallback = null) => {
  const LazyComponent = lazy(importFunc);
  
  return function WrappedComponent(props) {
    return (
      <Suspense fallback={fallback || <ComponentLoader />}>
        <LazyComponent {...props} />
      </Suspense>
    );
  };
};

const ComponentLoader = () => (
  <div className="flex items-center justify-center p-8">
    <Loader2 className="h-8 w-8 animate-spin" />
    <span className="ml-2">Loading...</span>
  </div>
);

export { createLazyComponent, ComponentLoader };
```

#### 3.2 Bundle Analysis Setup

**File: `webui/scripts/analyze-bundle.js`**

```javascript
#!/usr/bin/env node
import { execSync } from 'child_process';
import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

const BUNDLE_SIZE_LIMIT = 1024 * 1024; // 1MB
const CHUNK_SIZE_LIMIT = 512 * 1024; // 512KB

function analyzeBundleSize() {
  console.log('📊 Analyzing bundle size...');
  
  try {
    // Build with analysis
    execSync('npm run build', { stdio: 'inherit' });
    
    // Read bundle stats
    const statsPath = join(process.cwd(), 'dist', 'stats.html');
    const distPath = join(process.cwd(), 'dist');
    
    // Get file sizes
    const files = execSync(`find ${distPath} -name "*.js" -o -name "*.css"`, { 
      encoding: 'utf8' 
    }).trim().split('\n');
    
    const analysis = {
      timestamp: new Date().toISOString(),
      files: [],
      totalSize: 0,
      warnings: [],
      recommendations: []
    };
    
    files.forEach(file => {
      const size = execSync(`stat -c%s "${file}"`, { encoding: 'utf8' }).trim();
      const sizeBytes = parseInt(size);
      const fileName = file.replace(distPath + '/', '');
      
      analysis.files.push({
        name: fileName,
        size: sizeBytes,
        sizeFormatted: formatBytes(sizeBytes)
      });
      
      analysis.totalSize += sizeBytes;
      
      // Check for warnings
      if (sizeBytes > CHUNK_SIZE_LIMIT) {
        analysis.warnings.push({
          type: 'large_chunk',
          file: fileName,
          size: formatBytes(sizeBytes),
          message: `File exceeds recommended size limit (${formatBytes(CHUNK_SIZE_LIMIT)})`
        });
      }
    });
    
    // Generate recommendations
    if (analysis.totalSize > BUNDLE_SIZE_LIMIT) {
      analysis.recommendations.push({
        type: 'bundle_size',
        message: 'Consider implementing code splitting or removing unused dependencies',
        priority: 'high'
      });
    }
    
    // Save analysis
    writeFileSync(
      join(process.cwd(), 'bundle-analysis.json'),
      JSON.stringify(analysis, null, 2)
    );
    
    // Display results
    console.log('\n📋 Bundle Analysis Results:');
    console.log(`Total Bundle Size: ${formatBytes(analysis.totalSize)}`);
    console.log(`Number of Files: ${analysis.files.length}`);
    
    if (analysis.warnings.length > 0) {
      console.log('\n⚠️  Warnings:');
      analysis.warnings.forEach(warning => {
        console.log(`  - ${warning.file}: ${warning.message}`);
      });
    }
    
    if (analysis.recommendations.length > 0) {
      console.log('\n💡 Recommendations:');
      analysis.recommendations.forEach(rec => {
        console.log(`  - ${rec.message} (${rec.priority} priority)`);
      });
    }
    
    console.log(`\n📈 Detailed analysis saved to bundle-analysis.json`);
    console.log(`📊 Visual analysis available at dist/stats.html`);
    
  } catch (error) {
    console.error('❌ Bundle analysis failed:', error.message);
    process.exit(1);
  }
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

analyzeBundleSize();
```

#### 3.3 Performance Monitoring

**File: `webui/src/utils/performance.js`**

```javascript
class PerformanceMonitor {
  constructor() {
    this.metrics = new Map();
    this.observers = new Map();
    this.setupObservers();
  }

  setupObservers() {
    // Performance Observer for navigation timing
    if ('PerformanceObserver' in window) {
      const navObserver = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
          if (entry.entryType === 'navigation') {
            this.recordMetric('navigation', {
              domContentLoaded: entry.domContentLoadedEventEnd - entry.domContentLoadedEventStart,
              loadComplete: entry.loadEventEnd - entry.loadEventStart,
              firstPaint: entry.domContentLoadedEventEnd,
              type: entry.type
            });
          }
        });
      });
      
      try {
        navObserver.observe({ entryTypes: ['navigation'] });
        this.observers.set('navigation', navObserver);
      } catch (e) {
        console.warn('Navigation timing observer not supported');
      }
    }

    // Performance Observer for resource timing
    if ('PerformanceObserver' in window) {
      const resourceObserver = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
          if (entry.entryType === 'resource') {
            this.recordResourceMetric(entry);
          }
        });
      });
      
      try {
        resourceObserver.observe({ entryTypes: ['resource'] });
        this.observers.set('resource', resourceObserver);
      } catch (e) {
        console.warn('Resource timing observer not supported');
      }
    }
  }

  recordMetric(name, value) {
    if (!this.metrics.has(name)) {
      this.metrics.set(name, []);
    }
    
    this.metrics.get(name).push({
      value,
      timestamp: performance.now()
    });
  }

  recordResourceMetric(entry) {
    const resourceData = {
      name: entry.name,
      duration: entry.duration,
      size: entry.transferSize,
      type: this.getResourceType(entry.name),
      timestamp: entry.startTime
    };
    
    this.recordMetric('resources', resourceData);
  }

  getResourceType(url) {
    if (url.includes('.js')) return 'javascript';
    if (url.includes('.css')) return 'stylesheet';
    if (url.match(/\.(png|jpg|jpeg|gif|svg|webp)$/)) return 'image';
    if (url.includes('.woff') || url.includes('.ttf')) return 'font';
    return 'other';
  }

  measureComponentRender(componentName, renderFunction) {
    const startTime = performance.now();
    
    try {
      const result = renderFunction();
      
      if (result && typeof result.then === 'function') {
        // Handle async components
        return result.then((asyncResult) => {
          const endTime = performance.now();
          this.recordMetric('component_render', {
            name: componentName,
            duration: endTime - startTime,
            async: true
          });
          return asyncResult;
        });
      } else {
        // Handle sync components
        const endTime = performance.now();
        this.recordMetric('component_render', {
          name: componentName,
          duration: endTime - startTime,
          async: false
        });
        return result;
      }
    } catch (error) {
      const endTime = performance.now();
      this.recordMetric('component_render', {
        name: componentName,
        duration: endTime - startTime,
        error: error.message
      });
      throw error;
    }
  }

  getMetrics() {
    const report = {};
    
    this.metrics.forEach((values, key) => {
      report[key] = {
        count: values.length,
        values: values.slice(-10), // Last 10 values
        average: values.reduce((sum, item) => {
          const value = typeof item.value === 'object' ? item.value.duration : item.value;
          return sum + (value || 0);
        }, 0) / values.length
      };
    });
    
    return report;
  }

  reportToAnalytics() {
    const metrics = this.getMetrics();
    
    // Send to analytics service
    if (window.gtag) {
      Object.entries(metrics).forEach(([key, data]) => {
        window.gtag('event', 'performance_metric', {
          event_category: 'Performance',
          event_label: key,
          value: Math.round(data.average)
        });
      });
    }
    
    // Send to backend
    fetch('/api/performance/metrics', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        metrics,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent
      })
    }).catch(error => {
      console.warn('Failed to send performance metrics:', error);
    });
  }

  startPerformanceTracking() {
    // Report metrics every 30 seconds
    setInterval(() => {
      this.reportToAnalytics();
    }, 30000);
    
    // Report on page unload
    window.addEventListener('beforeunload', () => {
      this.reportToAnalytics();
    });
  }
}

// Create singleton instance
const performanceMonitor = new PerformanceMonitor();

// HOC for component performance monitoring
export const withPerformanceMonitoring = (WrappedComponent, componentName) => {
  return function PerformanceMonitoredComponent(props) {
    return performanceMonitor.measureComponentRender(
      componentName || WrappedComponent.name,
      () => <WrappedComponent {...props} />
    );
  };
};

export default performanceMonitor;
```

### Phase 4: Advanced Build Features (Week 4-5)

#### 4.1 Progressive Web App Configuration

**File: `webui/vite-plugin-pwa.config.js`**

```javascript
import { VitePWA } from 'vite-plugin-pwa';

export const pwaConfig = VitePWA({
  registerType: 'autoUpdate',
  workbox: {
    globPatterns: ['**/*.{js,css,html,ico,png,svg,woff,woff2}'],
    runtimeCaching: [
      {
        urlPattern: /^https:\/\/api\.piwardrive\.com\//,
        handler: 'NetworkFirst',
        options: {
          cacheName: 'api-cache',
          expiration: {
            maxEntries: 100,
            maxAgeSeconds: 60 * 60 * 24 // 24 hours
          }
        }
      },
      {
        urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp)$/,
        handler: 'CacheFirst',
        options: {
          cacheName: 'image-cache',
          expiration: {
            maxEntries: 50,
            maxAgeSeconds: 60 * 60 * 24 * 7 // 7 days
          }
        }
      }
    ]
  },
  manifest: {
    name: 'PiWardrive',
    short_name: 'PiWardrive',
    description: 'Advanced Raspberry Pi monitoring and management platform',
    theme_color: '#ffffff',
    background_color: '#ffffff',
    display: 'standalone',
    orientation: 'portrait',
    scope: '/',
    start_url: '/',
    icons: [
      {
        src: '/icon-192x192.png',
        sizes: '192x192',
        type: 'image/png'
      },
      {
        src: '/icon-512x512.png',
        sizes: '512x512',
        type: 'image/png'
      }
    ]
  },
  devOptions: {
    enabled: true
  }
});
```

#### 4.2 Build Pipeline Automation

**File: `webui/scripts/build-pipeline.js`**

```javascript
#!/usr/bin/env node
import { execSync } from 'child_process';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

const BUILD_STAGES = [
  'clean',
  'lint',
  'type-check',
  'test',
  'build',
  'analyze',
  'optimize'
];

class BuildPipeline {
  constructor() {
    this.buildMetrics = {
      startTime: Date.now(),
      stages: {},
      success: true,
      errors: []
    };
  }

  async runStage(stageName, command, options = {}) {
    console.log(`\n🚀 Running stage: ${stageName}`);
    const stageStart = Date.now();
    
    try {
      const result = execSync(command, {
        stdio: 'inherit',
        cwd: process.cwd(),
        ...options
      });
      
      const duration = Date.now() - stageStart;
      this.buildMetrics.stages[stageName] = {
        success: true,
        duration,
        command
      };
      
      console.log(`✅ Stage ${stageName} completed in ${duration}ms`);
      return result;
      
    } catch (error) {
      const duration = Date.now() - stageStart;
      this.buildMetrics.stages[stageName] = {
        success: false,
        duration,
        command,
        error: error.message
      };
      
      this.buildMetrics.success = false;
      this.buildMetrics.errors.push({
        stage: stageName,
        error: error.message
      });
      
      console.error(`❌ Stage ${stageName} failed after ${duration}ms`);
      throw error;
    }
  }

  async clean() {
    await this.runStage('clean', 'rm -rf dist node_modules/.vite');
  }

  async lint() {
    await this.runStage('lint', 'npm run lint');
  }

  async typeCheck() {
    await this.runStage('type-check', 'npm run type-check');
  }

  async test() {
    await this.runStage('test', 'npm run test:coverage');
  }

  async build() {
    await this.runStage('build', 'vite build');
  }

  async analyze() {
    await this.runStage('analyze', 'node scripts/analyze-bundle.js');
  }

  async optimize() {
    console.log('\n🔧 Optimizing build output...');
    
    // Compress assets
    await this.runStage('compress', 'gzip -k dist/*.js dist/*.css');
    
    // Generate build manifest
    this.generateBuildManifest();
  }

  generateBuildManifest() {
    const manifest = {
      buildTime: new Date().toISOString(),
      version: process.env.npm_package_version,
      environment: process.env.NODE_ENV || 'production',
      metrics: this.buildMetrics
    };
    
    writeFileSync(
      join(process.cwd(), 'dist', 'build-manifest.json'),
      JSON.stringify(manifest, null, 2)
    );
  }

  generateReport() {
    const totalDuration = Date.now() - this.buildMetrics.startTime;
    
    console.log('\n📊 Build Pipeline Report');
    console.log('========================');
    console.log(`Total Duration: ${totalDuration}ms`);
    console.log(`Status: ${this.buildMetrics.success ? '✅ SUCCESS' : '❌ FAILED'}`);
    
    console.log('\n📋 Stage Performance:');
    Object.entries(this.buildMetrics.stages).forEach(([stage, data]) => {
      const status = data.success ? '✅' : '❌';
      console.log(`  ${status} ${stage}: ${data.duration}ms`);
    });
    
    if (this.buildMetrics.errors.length > 0) {
      console.log('\n❌ Errors:');
      this.buildMetrics.errors.forEach(error => {
        console.log(`  - ${error.stage}: ${error.error}`);
      });
    }
    
    // Save report
    writeFileSync(
      join(process.cwd(), 'build-report.json'),
      JSON.stringify(this.buildMetrics, null, 2)
    );
  }

  async run() {
    try {
      console.log('🏗️  Starting build pipeline...');
      
      for (const stage of BUILD_STAGES) {
        await this[stage]();
      }
      
      console.log('\n🎉 Build pipeline completed successfully!');
      
    } catch (error) {
      console.error('\n💥 Build pipeline failed:', error.message);
      process.exit(1);
    } finally {
      this.generateReport();
    }
  }
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  const pipeline = new BuildPipeline();
  pipeline.run();
}

export default BuildPipeline;
```

#### 4.3 Development Server Enhancements

**File: `webui/scripts/dev-server.js`**

```javascript
#!/usr/bin/env node
import { createServer } from 'vite';
import { resolve } from 'path';
import { readFileSync } from 'fs';

const DEV_SERVER_CONFIG = {
  server: {
    port: 3000,
    host: true,
    open: true,
    cors: true,
    hmr: {
      overlay: true,
      port: 24678
    },
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  optimizeDeps: {
    force: true
  }
};

class DevServer {
  constructor() {
    this.server = null;
    this.startTime = Date.now();
  }

  async start() {
    console.log('🚀 Starting development server...');
    
    try {
      // Create Vite server
      this.server = await createServer({
        ...DEV_SERVER_CONFIG,
        configFile: resolve(process.cwd(), 'vite.config.js')
      });
      
      // Start server
      await this.server.listen();
      
      const startup = Date.now() - this.startTime;
      console.log(`✅ Development server started in ${startup}ms`);
      
      // Setup cleanup
      this.setupCleanup();
      
      // Log server info
      this.server.printUrls();
      
    } catch (error) {
      console.error('❌ Failed to start development server:', error);
      process.exit(1);
    }
  }

  setupCleanup() {
    const cleanup = () => {
      if (this.server) {
        console.log('\n🛑 Shutting down development server...');
        this.server.close();
      }
      process.exit(0);
    };
    
    process.on('SIGINT', cleanup);
    process.on('SIGTERM', cleanup);
  }

  async restart() {
    console.log('🔄 Restarting development server...');
    
    if (this.server) {
      await this.server.close();
    }
    
    this.startTime = Date.now();
    await this.start();
  }
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  const devServer = new DevServer();
  devServer.start();
}

export default DevServer;
```

### Phase 5: Testing and Deployment (Week 5-6)

#### 5.1 Vitest Configuration

**File: `webui/vitest.config.js`**

```javascript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    globals: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.js',
        'dist/'
      ]
    }
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@components': resolve(__dirname, 'src/components'),
      '@pages': resolve(__dirname, 'src/pages'),
      '@utils': resolve(__dirname, 'src/utils'),
      '@services': resolve(__dirname, 'src/services'),
      '@hooks': resolve(__dirname, 'src/hooks'),
      '@assets': resolve(__dirname, 'src/assets')
    }
  }
});
```

#### 5.2 CI/CD Integration

**File: `.github/workflows/frontend-build.yml`**

```yaml
name: Frontend Build and Test

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'webui/**'
  pull_request:
    branches: [ main, develop ]
    paths:
      - 'webui/**'

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [18.x, 20.x]
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
          cache-dependency-path: 'webui/package-lock.json'
      
      - name: Install dependencies
        run: |
          cd webui
          npm ci
      
      - name: Run linting
        run: |
          cd webui
          npm run lint
      
      - name: Run type checking
        run: |
          cd webui
          npm run type-check
      
      - name: Run tests
        run: |
          cd webui
          npm run test:coverage
      
      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
        with:
          file: ./webui/coverage/coverage-final.json
          flags: frontend
      
      - name: Build application
        run: |
          cd webui
          npm run build
      
      - name: Run bundle analysis
        run: |
          cd webui
          npm run analyze
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build-artifacts-${{ matrix.node-version }}
          path: |
            webui/dist/
            webui/bundle-analysis.json
            webui/build-report.json
      
      - name: Deploy to staging
        if: github.ref == 'refs/heads/develop'
        run: |
          # Deploy to staging environment
          echo "Deploying to staging..."
      
      - name: Deploy to production
        if: github.ref == 'refs/heads/main'
        run: |
          # Deploy to production environment
          echo "Deploying to production..."
```

## Implementation Checklist

### Week 1-2: Modern Build Setup

- [ ] Migrate from Create React App to Vite
- [ ] Configure TypeScript with strict settings
- [ ] Set up ESLint and Prettier
- [ ] Implement path aliases
- [ ] Configure development server with HMR

### Week 2-3: Developer Experience

- [ ] Set up hot module replacement
- [ ] Configure development tools
- [ ] Implement code formatting automation
- [ ] Set up pre-commit hooks
- [ ] Create development scripts

### Week 3-4: Build Optimization

- [ ] Implement code splitting
- [ ] Set up bundle analysis
- [ ] Configure performance monitoring
- [ ] Optimize asset loading
- [ ] Enable tree shaking

### Week 4-5: Advanced Features

- [ ] Configure Progressive Web App
- [ ] Set up build pipeline automation
- [ ] Implement caching strategies
- [ ] Create deployment scripts
- [ ] Set up monitoring and analytics

### Week 5-6: Testing and Deployment

- [ ] Configure Vitest testing framework
- [ ] Set up CI/CD pipeline
- [ ] Implement automated testing
- [ ] Configure deployment automation
- [ ] Set up monitoring and alerts

## Performance Targets

### Build Performance

- **Development server startup**: < 3 seconds
- **Hot module replacement**: < 100ms
- **Production build**: < 2 minutes
- **Bundle analysis**: < 30 seconds

### Runtime Performance

- **First Contentful Paint**: < 1.5 seconds
- **Largest Contentful Paint**: < 2.5 seconds
- **Cumulative Layout Shift**: < 0.1
- **First Input Delay**: < 100ms

### Bundle Optimization

- **Main bundle size**: < 1MB
- **Chunk size**: < 500KB
- **Code splitting**: 90% of routes lazy-loaded
- **Tree shaking**: 95% unused code removed

## Success Metrics

1. **Developer Experience**: 80% reduction in build time
2. **Performance**: 90% improvement in lighthouse scores
3. **Bundle Optimization**: 60% reduction in bundle size
4. **Reliability**: 99% successful builds in CI/CD
5. **Maintenance**: 70% reduction in build-related issues

## Monitoring and Maintenance

### Daily Monitoring

- Build pipeline success rate
- Bundle size trends
- Performance metrics
- Error rates and types

### Weekly Reviews

- Bundle analysis reports
- Performance regression analysis
- Dependency updates impact
- Developer feedback collection

### Monthly Optimization

- Build pipeline optimization
- Performance benchmark updates
- Tool and dependency upgrades
- Process improvement implementation

This comprehensive frontend build process streamlining plan will significantly improve developer experience, application performance, and deployment reliability while maintaining code quality and reducing maintenance overhead.
