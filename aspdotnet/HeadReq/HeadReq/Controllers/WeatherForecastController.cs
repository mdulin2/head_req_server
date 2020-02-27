using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace HeadReq.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class WeatherForecastController : ControllerBase
    {
        private static readonly string[] Summaries = new[]
        {
            "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
        };

        private readonly ILogger<WeatherForecastController> _logger;

        public WeatherForecastController(ILogger<WeatherForecastController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public String Get()
        {
            Console.WriteLine("GET");
            return "GET";
        }

        [HttpPost]
        public String Post()
        {
            Console.WriteLine("POST");
            return "POST";
        }

        [HttpPatch]
        public String Patch()
        {
            Console.WriteLine("PATCH");
            return "PATCH";
        }

        [HttpPut]
        public String Put()
        {
            Console.WriteLine("PUT");
            return "PUT";
        }

        [HttpDelete]
        public String Delete()
        {
            Console.WriteLine("DELETE");
            return "DELETE";
        }

        [HttpOptions]
        public String Options()
        {
            Console.WriteLine("OPTIONS");
            return "OPTIONS";
        }

        
        [HttpHead]
        public String Head()
        {
            return "HEAD";
        }
        
    }
}
