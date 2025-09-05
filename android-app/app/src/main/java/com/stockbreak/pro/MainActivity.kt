package com.stockbreak.pro

import android.annotation.SuppressLint
import android.content.Intent
import android.graphics.Bitmap
import android.net.Uri
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.webkit.*
import android.widget.Toast
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import com.stockbreak.pro.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding
    private var backPressedTime: Long = 0
    private val backPressInterval: Long = 2000
    
    override fun onCreate(savedInstanceState: Bundle?) {
        // Install splash screen
        installSplashScreen()
        
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        setupToolbar()
        setupWebView()
        setupSwipeRefresh()
        setupBackPressHandler()
        
        // Load StockBreak Pro web app
        loadStockBreakPro()
    }
    
    private fun setupToolbar() {
        setSupportActionBar(binding.toolbar)
        supportActionBar?.apply {
            title = "StockBreak Pro"
            subtitle = "AI-Powered Stock Analysis"
        }
    }
    
    @SuppressLint("SetJavaScriptEnabled")
    private fun setupWebView() {
        binding.webView.apply {
            settings.apply {
                javaScriptEnabled = true
                domStorageEnabled = true
                databaseEnabled = true
                allowFileAccess = true
                allowContentAccess = true
                setSupportZoom(true)
                builtInZoomControls = true
                displayZoomControls = false
                useWideViewPort = true
                loadWithOverviewMode = true
                cacheMode = WebSettings.LOAD_DEFAULT
                mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
            }
            
            webViewClient = StockBreakWebViewClient()
            webChromeClient = StockBreakWebChromeClient()
            
            // Add JavaScript interface for native integration
            addJavascriptInterface(WebAppInterface(this@MainActivity), "Android")
        }
    }
    
    private fun setupSwipeRefresh() {
        binding.swipeRefresh.apply {
            setColorSchemeResources(
                R.color.primary_color,
                R.color.secondary_color
            )
            
            setOnRefreshListener {
                binding.webView.reload()
            }
        }
    }
    
    private fun setupBackPressHandler() {
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                when {
                    binding.webView.canGoBack() -> {
                        binding.webView.goBack()
                    }
                    backPressedTime + backPressInterval > System.currentTimeMillis() -> {
                        finish()
                    }
                    else -> {
                        Toast.makeText(
                            this@MainActivity, 
                            "Press back again to exit", 
                            Toast.LENGTH_SHORT
                        ).show()
                        backPressedTime = System.currentTimeMillis()
                    }
                }
            }
        })
    }
    
    private fun loadStockBreakPro() {
        val webAppUrl = if (BuildConfig.DEBUG) {
            "http://10.0.2.2:3000"  // Development server
        } else {
            BuildConfig.WEB_APP_URL  // Production URL
        }
        
        binding.webView.loadUrl(webAppUrl)
    }
    
    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.main_menu, menu)
        return true
    }
    
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_refresh -> {
                binding.webView.reload()
                true
            }
            R.id.action_settings -> {
                startActivity(Intent(this, SettingsActivity::class.java))
                true
            }
            R.id.action_share -> {
                shareApp()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
    
    private fun shareApp() {
        val shareIntent = Intent().apply {
            action = Intent.ACTION_SEND
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, 
                "Check out StockBreak Pro - AI-Powered Stock Analysis!\n" +
                "Professional technical & fundamental analysis for Indian markets.\n" +
                "Download: https://play.google.com/store/apps/details?id=com.stockbreak.pro")
        }
        startActivity(Intent.createChooser(shareIntent, "Share StockBreak Pro"))
    }
    
    // WebView Client for handling page navigation
    private inner class StockBreakWebViewClient : WebViewClient() {
        
        override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
            val url = request?.url.toString()
            
            return when {
                url.startsWith("http://") || url.startsWith("https://") -> {
                    // Handle external links
                    if (url.contains("stockbreak") || url.contains("localhost") || url.contains("10.0.2.2")) {
                        false  // Load in WebView
                    } else {
                        // Open external links in browser
                        startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
                        true
                    }
                }
                else -> false
            }
        }
        
        override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
            super.onPageStarted(view, url, favicon)
            binding.swipeRefresh.isRefreshing = true
        }
        
        override fun onPageFinished(view: WebView?, url: String?) {
            super.onPageFinished(view, url)
            binding.swipeRefresh.isRefreshing = false
            
            // Inject mobile-optimized CSS
            injectMobileCSS()
        }
        
        override fun onReceivedError(view: WebView?, request: WebResourceRequest?, error: WebResourceError?) {
            super.onReceivedError(view, request, error)
            binding.swipeRefresh.isRefreshing = false
            
            // Show error message
            Toast.makeText(
                this@MainActivity,
                "Connection error. Please check your internet connection.",
                Toast.LENGTH_LONG
            ).show()
        }
    }
    
    // Chrome Client for handling JavaScript dialogs and progress
    private inner class StockBreakWebChromeClient : WebChromeClient() {
        
        override fun onProgressChanged(view: WebView?, newProgress: Int) {
            super.onProgressChanged(view, newProgress)
            binding.swipeRefresh.isRefreshing = newProgress < 100
        }
        
        override fun onJsAlert(view: WebView?, url: String?, message: String?, result: JsResult?): Boolean {
            Toast.makeText(this@MainActivity, message, Toast.LENGTH_LONG).show()
            result?.confirm()
            return true
        }
    }
    
    private fun injectMobileCSS() {
        val css = """
            javascript:(function() {
                var style = document.createElement('style');
                style.innerHTML = `
                    /* Mobile optimizations for StockBreak Pro */
                    body { 
                        -webkit-text-size-adjust: 100%; 
                        font-size: 14px !important;
                    }
                    .table-container { 
                        overflow-x: auto; 
                        -webkit-overflow-scrolling: touch;
                    }
                    button, .btn { 
                        min-height: 44px; 
                        padding: 12px 16px;
                    }
                    input, select { 
                        min-height: 44px; 
                        font-size: 16px;
                    }
                    .card { 
                        margin: 8px; 
                        border-radius: 12px;
                    }
                    /* Hide desktop-only elements */
                    @media (max-width: 768px) {
                        .desktop-only { display: none !important; }
                        .mobile-hidden { display: none !important; }
                    }
                `;
                document.head.appendChild(style);
            })();
        """
        
        binding.webView.evaluateJavascript(css, null)
    }
    
    // JavaScript Interface for native app integration
    inner class WebAppInterface(private val context: MainActivity) {
        
        @JavascriptInterface
        fun showToast(message: String) {
            runOnUiThread {
                Toast.makeText(context, message, Toast.LENGTH_SHORT).show()
            }
        }
        
        @JavascriptInterface
        fun shareStock(stockSymbol: String, stockName: String, price: String) {
            runOnUiThread {
                val shareText = "Check out $stockName ($stockSymbol) at ₹$price on StockBreak Pro!"
                val shareIntent = Intent().apply {
                    action = Intent.ACTION_SEND
                    type = "text/plain"
                    putExtra(Intent.EXTRA_TEXT, shareText)
                }
                context.startActivity(Intent.createChooser(shareIntent, "Share Stock"))
            }
        }
    }
}